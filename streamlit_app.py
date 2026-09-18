"""People Finder — Streamlit port of the browser OSINT dork builder."""

from __future__ import annotations

import json
import re
import urllib.parse
from typing import Any

import requests
import streamlit as st

PLATFORMS: dict[str, str] = {
    "LinkedIn": "linkedin.com",
    "Facebook": "facebook.com",
    "X": "(site:x.com OR site:twitter.com)",
    "Reddit": "reddit.com",
    "Instagram": "instagram.com",
    "TikTok": "tiktok.com",
    "Threads": "threads.com",
    "Google": "",
}

GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)


def build_dork(name: str, clue: str, site: str) -> str:
    clean_name = re.sub(r"\s+", " ", name.strip())
    clean_clue = re.sub(r"\s+", " ", clue.strip())

    if site:
        site_prefix = f"{site} " if "site:" in site else f"site:{site} "
    else:
        site_prefix = ""

    if not clean_name and not clean_clue:
        return f'{site_prefix}"name" "clue"'.strip()
    if clean_name and clean_clue:
        return f'{site_prefix}"{clean_name}" "{clean_clue}"'.strip()
    if clean_name:
        return f'{site_prefix}"{clean_name}"'.strip()
    return f'{site_prefix}"{clean_clue}"'.strip()


def google_search_url(dork: str) -> str:
    return "https://www.google.com/search?q=" + urllib.parse.quote(dork)


def parse_gemini_json(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    return json.loads(cleaned)


def suggest_with_gemini(
    api_key: str,
    platform: str,
    name: str,
    clue: str,
    dork: str,
) -> dict[str, Any]:
    prompt = "\n".join(
        [
            "You help build Google OSINT people-search dorks.",
            "Return ONLY valid JSON with this shape:",
            '{"clues":["..."],"nameVariations":["..."],"tips":["..."]}',
            "Give 4-6 short searchable clues (job, company, city, school, username-style keywords).",
            "Give 3-5 realistic name spelling / abbreviation variations.",
            "Give 2-4 practical search tips for the selected platform.",
            "Do not invent private facts. Keep strings concise for Google queries.",
            f"Platform: {platform}",
            f"Name: {name or '(none)'}",
            f"Clue: {clue or '(none)'}",
            f"Current dork: {dork}",
        ]
    )

    response = requests.post(
        GEMINI_URL,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.4,
                "responseMimeType": "application/json",
            },
        },
        timeout=60,
    )

    payload = response.json() if response.content else {}
    if not response.ok:
        message = (
            payload.get("error", {}).get("message")
            or f"Gemini request failed ({response.status_code})"
        )
        raise RuntimeError(message)

    parts = (
        payload.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [])
    )
    text = "".join(part.get("text", "") for part in parts).strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return parse_gemini_json(text)


def get_secret_gemini_key() -> str:
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "") or "").strip()
    except Exception:
        return ""


def init_state() -> None:
    defaults = {
        "full_name": "johndoe",
        "clue": "penetration tester",
        "platform": "LinkedIn",
        "gemini_key": "",
        "gemini_suggestions": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main() -> None:
    st.set_page_config(
        page_title="People Finder",
        page_icon="🔍",
        layout="centered",
    )
    init_state()

    st.title("People Finder")
    st.caption("Build Google dorks · name + clue · pick a platform · optional Gemini")

    platform = st.radio(
        "Platform",
        list(PLATFORMS.keys()),
        horizontal=True,
        key="platform",
        help="Searches via Google with site: (Google = web-wide)",
    )

    name = st.text_input(
        "Full name",
        key="full_name",
        placeholder="e.g. johndoe",
        help="Use exact name or variations",
    )
    clue = st.text_input(
        "Clue / info",
        key="clue",
        placeholder="e.g. penetration tester, security researcher",
        help="Any keyword: job, location, interest, company",
    )

    site = PLATFORMS[platform]
    dork = build_dork(name, clue, site)
    search_url = google_search_url(dork)

    st.subheader("Dork preview")
    st.code(dork, language=None)
    st.link_button("Search with Dork", search_url, type="primary", use_container_width=True)

    with st.expander("Gemini assist (optional)", expanded=False):
        st.markdown(
            "Get a key at [Google AI Studio](https://aistudio.google.com/apikey). "
            "On Streamlit Cloud you can set `GEMINI_API_KEY` in **App settings → Secrets** "
            "(server-side only — not shown in this field). Or paste your own key below."
        )
        has_secret = bool(get_secret_gemini_key())
        if has_secret:
            st.info("A server-side `GEMINI_API_KEY` secret is configured for this app.")

        st.text_input(
            "Gemini API key (optional override)",
            key="gemini_key",
            type="password",
            placeholder="Paste your own key, or leave blank to use app secret",
            help="Optional. Prefer Streamlit secrets on a public Cloud app so the shared key is not exposed in the browser.",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            suggest = st.button("Suggest with Gemini", use_container_width=True)
        with col_b:
            if st.button("Clear pasted key", use_container_width=True):
                st.session_state.gemini_key = ""
                st.session_state.gemini_suggestions = None
                st.rerun()

        if suggest:
            api_key = st.session_state.gemini_key.strip() or get_secret_gemini_key()
            if not api_key:
                st.error("Add a Gemini API key, or set GEMINI_API_KEY in Streamlit secrets.")
            elif not name.strip() and not clue.strip():
                st.error("Enter a name and/or clue before asking Gemini.")
            else:
                with st.spinner("Asking Gemini…"):
                    try:
                        data = suggest_with_gemini(
                            api_key, platform, name.strip(), clue.strip(), dork
                        )
                        st.session_state.gemini_suggestions = data
                        st.success("Suggestions ready — click a chip to apply.")
                    except Exception as exc:
                        st.error(str(exc))

        data = st.session_state.gemini_suggestions
        if data:
            clues = [str(c).strip() for c in (data.get("clues") or []) if str(c).strip()]
            names = [
                str(n).strip()
                for n in (data.get("nameVariations") or [])
                if str(n).strip()
            ]
            tips = [str(t).strip() for t in (data.get("tips") or []) if str(t).strip()]

            if clues:
                st.markdown("**Suggested clues**")
                cols = st.columns(min(3, len(clues)))
                for i, item in enumerate(clues):
                    if cols[i % len(cols)].button(item, key=f"clue_chip_{i}"):
                        st.session_state.clue = item
                        st.rerun()

            if names:
                st.markdown("**Name variations**")
                cols = st.columns(min(3, len(names)))
                for i, item in enumerate(names):
                    if cols[i % len(cols)].button(item, key=f"name_chip_{i}"):
                        st.session_state.full_name = item
                        st.rerun()

            if tips:
                st.markdown("**Tips**")
                for tip in tips:
                    st.markdown(f"- {tip}")

    st.divider()
    st.caption(
        "Also available as static HTML (`index.html`). "
        "Repo: [jebat8101/People-Finder](https://github.com/jebat8101/People-Finder)"
    )


if __name__ == "__main__":
    main()

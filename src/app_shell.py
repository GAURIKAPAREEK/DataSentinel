"""App shell — theme init, CSS injection, header."""

from __future__ import annotations

import streamlit as st

from src.ui.components.header import render_header
from src.ui.components.theme_toggle import render_theme_toggle
from src.ui.stylesheet import build_global_css


def init_theme(default: str = "dark") -> None:
    if "theme" not in st.session_state:
        st.session_state.theme = default


# ─────────────────────────────────────────────────────────────────
# Force desktop layout on mobile: override Streamlit's default
# viewport meta so phones render the page at a fixed desktop width
# (1280px) and the browser scales it down. This makes the phone
# view look identical to the laptop view.
# ─────────────────────────────────────────────────────────────────
_FORCE_DESKTOP_VIEWPORT = """
<script>
(function () {
  try {
    var docs = [document];
    try {
      if (window.parent && window.parent.document && window.parent.document !== document) {
        docs.push(window.parent.document);
      }
    } catch (e) { /* cross-origin */ }
    docs.forEach(function (d) {
      var m = d.querySelector('meta[name="viewport"]');
      if (!m) {
        m = d.createElement('meta');
        m.setAttribute('name', 'viewport');
        d.head.appendChild(m);
      }
      m.setAttribute('content', 'width=1280, initial-scale=0.25, user-scalable=yes');
    });
  } catch (e) {}
})();
</script>
"""


import importlib
import src.ui.stylesheet

def inject_css(*, login: bool = False) -> None:
    importlib.reload(src.ui.stylesheet)
    css = src.ui.stylesheet.build_global_css(login=login)
    if hasattr(st, "html"):
        st.html(_FORCE_DESKTOP_VIEWPORT)
        st.html(css)
    else:
        st.markdown(_FORCE_DESKTOP_VIEWPORT, unsafe_allow_html=True)
        st.markdown(css, unsafe_allow_html=True)


def render_app_header(
    name: str,
    username: str,
    email: str = "",
    theme_key: str = "hdr_theme",
    logout_key: str = "hdr_logout",
) -> None:
    import importlib
    import src.ui.components.header
    importlib.reload(src.ui.components.header)
    src.ui.components.header.render_header(name, username, email, theme_key=theme_key, logout_key=logout_key)


def toggle_theme(key: str) -> None:
    render_theme_toggle(key)


def render_sidebar(_name: str) -> None:
    pass

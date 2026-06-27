import streamlit as st

def render_card(title: str, body: str, badge: str | None = None) -> None:
    """
    Renders a premium glassmorphic card component with a title, body description,
    and optional badge.
    """
    badge_html = f'<div class="aeterna-badge">{badge}</div>' if badge else ''
    card_html = f'<div class="aeterna-card"><div class="aeterna-card-header">{title}</div><div class="aeterna-card-body">{body}</div>{badge_html}</div>'
    st.markdown(card_html, unsafe_allow_html=True)


def render_stat_card(label: str, value: str, delta: str | None = None) -> None:
    """
    Renders a glassmorphic micro-card optimized for key statistics or metrics.
    """
    delta_html = f'<span style="color: #10b981; font-size: 0.8rem; font-weight: 600; margin-left: 8px;">↑ {delta}</span>' if delta else ''
    card_html = f'<div class="aeterna-card" style="padding: 16px; margin-bottom: 15px; min-height: 140px; display: flex; flex-direction: column; justify-content: space-between;"><div style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 500;">{label}</div><div style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; font-family:\'Outfit\', sans-serif; margin-top: 6px; display: block; line-height: 1.3; word-break: break-word; overflow-wrap: break-word;">{value}{delta_html}</div></div>'
    st.markdown(card_html, unsafe_allow_html=True)

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Countdown",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

VIDEO_URL = "https://ika.xyz/videos/hero-loop.mp4"

components.html(
    f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background: #000;
            }}

            #container {{
                position: relative;
                width: 100%;
                height: 100vh;
                overflow: hidden;
                background: #000;
            }}

            #video {{
                position: absolute;
                inset: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
                background: #000;
            }}

            #countdown {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 10;
                color: white;
                text-align: center;
                font-family: Arial, Helvetica, sans-serif;
                font-weight: 700;
                letter-spacing: 1px;
                text-shadow:
                    0 2px 12px rgba(0, 0, 0, 0.9),
                    0 0 25px rgba(0, 0, 0, 0.8);
                white-space: nowrap;
            }}

            #days {{
                font-size: clamp(38px, 7vw, 90px);
                line-height: 1.05;
            }}

            #label {{
                margin-top: 10px;
                font-size: clamp(13px, 1.7vw, 22px);
                font-weight: 500;
                opacity: 0.9;
            }}

            #expired {{
                display: none;
                font-size: clamp(40px, 7vw, 90px);
            }}
        </style>
    </head>

    <body>
        <div id="container">
            <video
                id="video"
                autoplay
                muted
                loop
                playsinline
                preload="auto"
            >
                <source src="{VIDEO_URL}" type="video/mp4">
                Your browser does not support HTML5 video.
            </video>

            <div id="countdown">
                <div id="days">Loading...</div>
                <div id="label">UNTIL 15 NOVEMBER 2026</div>
                <div id="expired">The countdown has ended.</div>
            </div>
        </div>

        <script>
            // Target: 15 November 2026 at 00:00:00 India Standard Time (UTC+05:30)
            const targetTime = new Date("2026-11-15T00:00:00+05:30").getTime();

            const countdownElement = document.getElementById("days");
            const labelElement = document.getElementById("label");
            const expiredElement = document.getElementById("expired");
            const video = document.getElementById("video");

            function updateCountdown() {{
                const now = Date.now();
                const difference = targetTime - now;

                if (difference <= 0) {{
                    countdownElement.style.display = "none";
                    labelElement.style.display = "none";
                    expiredElement.style.display = "block";
                    return;
                }}

                const totalSeconds = Math.floor(difference / 1000);

                const days = Math.floor(totalSeconds / 86400);
                const hours = Math.floor((totalSeconds % 86400) / 3600);
                const minutes = Math.floor((totalSeconds % 3600) / 60);
                const seconds = totalSeconds % 60;

                countdownElement.textContent =
                    `${{days}}d ${{String(hours).padStart(2, "0")}}h ` +
                    `${{String(minutes).padStart(2, "0")}}m ` +
                    `${{String(seconds).padStart(2, "0")}}s`;
            }}

            // Make a best effort to start the video.
            video.play().catch(() => {{
                // Autoplay can only be blocked by the browser if the video is not muted.
                // This video is intentionally muted so autoplay normally works.
            }});

            updateCountdown();
            setInterval(updateCountdown, 250);
        </script>
    </body>
    </html>
    """,
    height=700,
    scrolling=False,
)

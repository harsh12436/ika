import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Countdown",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove Streamlit's default margins/padding so the video fills the screen.
st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stApp"], .main {
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stAppViewContainer"] > .main > div {
            padding: 0 !important;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }

        iframe {
            display: block !important;
            width: 100vw !important;
            max-width: 100vw !important;
            border: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stHeader"],
        footer {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

VIDEO_URL = "https://ika.xyz/videos/hero-loop.mp4"

components.html(
    f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0, viewport-fit=cover">

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
                position: fixed;
                inset: 0;
                width: 100vw;
                height: 100vh;
                overflow: hidden;
                background: #000;
            }}

            /*
             * VIDEO
             * Desktop: fills the complete screen.
             * Mobile portrait: ONLY THE VIDEO is rotated 90 degrees.
             */
            #video {{
                position: absolute;
                top: 50%;
                left: 50%;
                width: 100vw;
                height: 100vh;
                transform: translate(-50%, -50%);
                object-fit: cover;
                display: block;
                background: #000;
            }}

            /* Pink/red tint over the video */
            #tint {{
                position: absolute;
                inset: 0;
                z-index: 2;
                pointer-events: none;
                background: rgba(145, 15, 55, 0.20);
                mix-blend-mode: screen;
            }}

            #shade {{
                position: absolute;
                inset: 0;
                z-index: 3;
                pointer-events: none;
                background: rgba(20, 0, 8, 0.12);
            }}

            /*
             * TIMER
             * IMPORTANT:
             * The timer is NEVER rotated.
             * It always stays upright and centered on the screen.
             */
            #countdown {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 10;
                color: #ffb6c8;
                text-align: center;
                font-family: Arial, Helvetica, sans-serif;
                font-weight: 700;
                letter-spacing: 1px;
                text-shadow:
                    0 2px 12px rgba(0, 0, 0, 0.95),
                    0 0 18px rgba(255, 40, 100, 0.75);
                white-space: nowrap;
            }}

            #days {{
                font-size: clamp(38px, 7vw, 90px);
                line-height: 1.05;
            }}

            #expired {{
                display: none;
                font-size: clamp(40px, 7vw, 90px);
            }}

            /*
             * MOBILE PORTRAIT
             *
             * Rotate ONLY the video and its visual overlays.
             * The timer is deliberately NOT rotated.
             */
            @media (max-width: 768px) and (orientation: portrait) {{
                #video {{
                    width: 100vh;
                    height: 100vw;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) rotate(90deg);
                }}

                #tint,
                #shade {{
                    width: 100vh;
                    height: 100vw;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) rotate(90deg);
                    transform-origin: center center;
                }}

                /* NO rotation here — timer stays upright */
                #countdown {{
                    transform: translate(-50%, -50%);
                }}

                #days {{
                    font-size: clamp(32px, 8vw, 65px);
                }}
            }}

            /*
             * MOBILE LANDSCAPE
             * Nothing is rotated.
             */
            @media (max-width: 900px) and (orientation: landscape) {{
                #video,
                #tint,
                #shade {{
                    width: 100vw;
                    height: 100vh;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                }}

                #countdown {{
                    transform: translate(-50%, -50%);
                }}

                #days {{
                    font-size: clamp(30px, 7vw, 70px);
                }}
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

            <div id="tint"></div>
            <div id="shade"></div>

            <!-- Timer stays upright on every orientation -->
            <div id="countdown">
                <div id="days">Loading...</div>
                <div id="expired">The countdown has ended.</div>
            </div>

        </div>

        <script>
            // Target: 15 November 2026, 00:00:00 IST (UTC+05:30)
            const targetTime =
                new Date("2026-11-15T00:00:00+05:30").getTime();

            const countdownElement =
                document.getElementById("days");

            const expiredElement =
                document.getElementById("expired");

            const video =
                document.getElementById("video");

            function updateCountdown() {{
                const difference = targetTime - Date.now();

                if (difference <= 0) {{
                    countdownElement.style.display = "none";
                    expiredElement.style.display = "block";
                    return;
                }}

                const totalSeconds =
                    Math.floor(difference / 1000);

                const days =
                    Math.floor(totalSeconds / 86400);

                const hours =
                    Math.floor((totalSeconds % 86400) / 3600);

                const minutes =
                    Math.floor((totalSeconds % 3600) / 60);

                const seconds =
                    totalSeconds % 60;

                countdownElement.textContent =
                    `${{days}}d ${{String(hours).padStart(2, "0")}}h ` +
                    `${{String(minutes).padStart(2, "0")}}m ` +
                    `${{String(seconds).padStart(2, "0")}}s`;
            }}

            // Muted autoplay normally works without user interaction.
            video.play().catch(() => {{}});

            updateCountdown();

            // Update the displayed seconds continuously.
            setInterval(updateCountdown, 250);
        </script>
    </body>
    </html>
    """,
    height=1000,
    scrolling=False,
)

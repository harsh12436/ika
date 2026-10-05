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
        <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
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
                min-height: 100vh;
                overflow: hidden;
                background: #000;
            }}

            #video {{
                position: absolute;
                top: 50%;
                left: 50%;
                width: 100%;
                height: 100%;
                transform: translate(-50%, -50%);
                object-fit: cover;
                display: block;
                background: #000;
            }}

            /* Pink/red tint over the entire video */
            #tint {{
                position: absolute;
                inset: 0;
                z-index: 2;
                pointer-events: none;
                background:
                    linear-gradient(
                        rgba(145, 15, 55, 0.28),
                        rgba(145, 15, 55, 0.28)
                    );
                mix-blend-mode: screen;
            }}

            /* Slight dark overlay so the timer remains readable */
            #shade {{
                position: absolute;
                inset: 0;
                z-index: 3;
                pointer-events: none;
                background: rgba(20, 0, 8, 0.16);
            }}

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
             * On a phone in portrait mode, rotate the video 90 degrees
             * and make it fill the screen in landscape orientation.
             * The timer stays centered relative to the rotated video.
             */
            @media (max-width: 768px) and (orientation: portrait) {{
                #video,
                #tint,
                #shade {{
                    width: 100vh;
                    height: 100vw;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) rotate(90deg);
                }}

                #tint,
                #shade {{
                    transform-origin: center center;
                }}

                #countdown {{
                    transform: translate(-50%, -50%) rotate(90deg);
                }}

                #days {{
                    font-size: clamp(32px, 8vw, 65px);
                }}
            }}

            /*
             * Landscape phones: fill the available screen.
             */
            @media (max-width: 900px) and (orientation: landscape) {{
                #video,
                #tint,
                #shade {{
                    width: 100vw;
                    height: 100vh;
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

            <div id="countdown">
                <div id="days">Loading...</div>
                <div id="expired">The countdown has ended.</div>
            </div>

        </div>

        <script>
            // 15 November 2026, 00:00:00 IST (UTC+05:30)
            const targetTime =
                new Date("2026-11-15T00:00:00+05:30").getTime();

            const countdownElement =
                document.getElementById("days");

            const expiredElement =
                document.getElementById("expired");

            const video =
                document.getElementById("video");

            function updateCountdown() {{
                const now = Date.now();
                const difference = targetTime - now;

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

            video.play().catch(() => {{
                // Muted autoplay should normally be allowed by browsers.
            }});

            updateCountdown();

            // Refresh frequently so the displayed seconds stay accurate.
            setInterval(updateCountdown, 250);
        </script>
    </body>
    </html>
    """,
    height=700,
    scrolling=False,
)

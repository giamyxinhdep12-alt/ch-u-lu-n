import streamlit as st
import streamlit.components.v1 as components
import html
import random
import base64
import os
import json


# ==========================================
# CẤU HÌNH TRANG
# ==========================================

st.set_page_config(
    page_title="Trường Đua Vịt",
    page_icon="🦆",
    layout="wide"
)


# ==========================================
# TIÊU ĐỀ
# ==========================================

st.title("🦆🏁 TRƯỜNG ĐUA VỊT 🏁🦆")
st.caption("Nhập tên người chơi và xem ai về đích trước!")


# ==========================================
# NHẬP TÊN
# ==========================================

text_names = st.text_area(
    "👥 Nhập tên người tham gia — tối đa 50 người",
    placeholder="Mỗi người một dòng\n\nAn\nBình\nChi\nDũng",
    height=180
)


names = [
    x.strip()
    for x in text_names.splitlines()
    if x.strip()
]


# Xóa tên trùng
names = list(dict.fromkeys(names))


# Giới hạn 50 người
if len(names) > 50:
    st.warning("⚠️ Chỉ được tối đa 50 người!")
    names = names[:50]


st.write(
    f"👥 Người tham gia: **{len(names)}/50**"
)


# ==========================================
# NÚT BẮT ĐẦU
# ==========================================

start = st.button(
    "🚀🏁 BẮT ĐẦU ĐUA! 🏁🚀",
    use_container_width=True
)


# ==========================================
# BẮT ĐẦU CUỘC ĐUA
# ==========================================

if start:

    if len(names) < 2:

        st.warning(
            "⚠️ Cần ít nhất 2 người để bắt đầu cuộc đua!"
        )

    else:

        # ==================================
        # ĐỌC NHẠC
        # ==================================

        music_data = ""

        music_path = "nhac.mp3"

        if os.path.exists(music_path):

            with open(music_path, "rb") as music_file:

                music_bytes = music_file.read()

            music_base64 = base64.b64encode(
                music_bytes
            ).decode("utf-8")

            music_data = (
                "data:audio/mpeg;base64,"
                + music_base64
            )

        else:

            st.warning(
                "⚠️ Không tìm thấy nhac.mp3. "
                "Hãy đặt file nhac.mp3 cùng thư mục với app."
            )


        # ==================================
        # MÀU LÀN ĐUA
        # ==================================

        lane_colors = [
            "#FFE5EC",
            "#E0F7FF",
            "#E8FFD9",
            "#FFF4CC",
            "#EDE0FF",
            "#FFE4CC",
            "#FFE8D6",
            "#E0FFE8"
        ]


        # ==================================
        # TẠO LÀN ĐUA
        # ==================================

        lanes = ""

        for i, name in enumerate(names):

            safe_name = html.escape(name)

            lanes += """
            <div
                class="lane"
                style="background:__LANE_COLOR__;"
            >

                <div class="name">
                    🦆 __PLAYER_NAME__
                </div>

                <div class="road">

                    <div
                        class="duck"
                        id="duck__INDEX__"
                    >
                        🦆
                    </div>

                    <div class="finish">
                        🏁
                    </div>

                </div>

            </div>
            """

            lanes = lanes.replace(
                "__LANE_COLOR__",
                lane_colors[i % len(lane_colors)],
                1
            )

            lanes = lanes.replace(
                "__PLAYER_NAME__",
                safe_name,
                1
            )

            lanes = lanes.replace(
                "__INDEX__",
                str(i),
                1
            )


        # ==================================
        # TỐC ĐỘ VỊT
        # ==================================

        speeds = [
            random.uniform(0.75, 2.1)
            for _ in names
        ]


        # ==================================
        # DỮ LIỆU JAVASCRIPT
        # ==================================

        names_js = json.dumps(
            names,
            ensure_ascii=False
        )

        speeds_js = json.dumps(
            speeds
        )


        # ==================================
        # HTML
        #
        # KHÔNG DÙNG F-STRING
        # => KHÔNG BỊ LỖI { }
        # ==================================

        race_html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    font-family: Arial, sans-serif;

    background: white;
}


/* ==================================
   MÀN HÌNH
================================== */

.screen {
    position: absolute;

    left: 0;
    top: 0;

    width: 100%;
    height: 100%;

    display: none;
}

.screen.active {
    display: flex;
}


/* ==================================
   COUNTDOWN
================================== */

#countScreen {
    align-items: center;
    justify-content: center;

    flex-direction: column;
}

#count {
    font-size: 110px;

    font-weight: 900;

    animation:
        countPop
        0.8s
        ease;
}

@keyframes countPop {

    0% {
        transform: scale(0.2);
        opacity: 0;
    }

    60% {
        transform: scale(1.25);
        opacity: 1;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}


/* ==================================
   TRƯỜNG ĐUA
================================== */

#raceScreen {
    flex-direction: column;

    padding: 10px;
}

#raceScreen.active {
    display: flex;
}

.title {
    text-align: center;

    font-size: 28px;

    font-weight: 900;

    margin-bottom: 8px;
}

#raceList {
    flex: 1;

    overflow-y: auto;

    overflow-x: hidden;

    padding-right: 5px;
}

#raceList::-webkit-scrollbar {
    width: 8px;
}

#raceList::-webkit-scrollbar-thumb {
    background: #bbbbbb;

    border-radius: 10px;
}


/* ==================================
   LÀN
================================== */

.lane {
    height: 48px;

    margin: 4px 0;

    padding: 4px;

    border-radius: 13px;

    display: flex;

    align-items: center;
}

.name {
    width: 125px;

    font-size: 14px;

    font-weight: bold;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}


/* ==================================
   ĐƯỜNG ĐUA
================================== */

.road {
    position: relative;

    flex: 1;

    height: 38px;

    border: 2px solid #555;

    border-radius: 9px;

    overflow: hidden;

    background:
        repeating-linear-gradient(
            90deg,
            #eeeeee 0px,
            #eeeeee 30px,
            #ffffff 30px,
            #ffffff 60px
        );
}


/* ==================================
   VỊT
================================== */

.duck {
    position: absolute;

    left: 0%;

    top: 0px;

    font-size: 28px;

    z-index: 5;
}


/* ==================================
   ĐÍCH
================================== */

.finish {
    position: absolute;

    right: 4px;

    top: 1px;

    font-size: 26px;
}


/* ==================================
   KẾT QUẢ
================================== */

#resultScreen {
    align-items: center;

    justify-content: center;

    flex-direction: column;

    padding: 15px;
}

#resultBox {
    width: min(620px, 94%);

    max-height: 90%;

    overflow-y: auto;

    padding: 22px;

    border-radius: 25px;

    background:
        linear-gradient(
            135deg,
            #fff7b8,
            #ffffff
        );

    border: 3px solid #ffd43b;

    box-shadow:
        0 8px 30px
        rgba(0,0,0,0.18);

    animation:
        resultPop
        0.7s
        ease;
}

@keyframes resultPop {

    from {
        transform: scale(0.5);

        opacity: 0;
    }

    to {
        transform: scale(1);

        opacity: 1;
    }
}

#resultBox h1 {
    margin: 0 0 18px;

    text-align: center;

    font-size: 30px;
}

.rank {
    margin: 7px 0;

    padding: 11px 14px;

    border-radius: 14px;

    background: white;

    font-size: 18px;

    font-weight: bold;

    box-shadow:
        0 2px 6px
        rgba(0,0,0,0.1);
}

.rank.first {
    background:
        linear-gradient(
            90deg,
            #ffe680,
            #fff8c7
        );

    font-size: 22px;
}


/* ==================================
   BÓNG BAY
================================== */

.balloon {
    position: fixed;

    left: 0;

    bottom: -80px;

    font-size: 35px;

    pointer-events: none;

    z-index: 9999;

    animation:
        balloonUp
        3.5s
        linear
        forwards;
}

@keyframes balloonUp {

    0% {
        transform:
            translateY(0)
            rotate(0deg);

        opacity: 1;
    }

    100% {
        transform:
            translateY(-750px)
            rotate(360deg);

        opacity: 0;
    }
}


/* ==================================
   NÚT NHẠC
================================== */

#musicButton {
    position: absolute;

    right: 12px;

    top: 10px;

    z-index: 10000;

    display: none;

    border: none;

    border-radius: 12px;

    padding: 9px 14px;

    font-size: 14px;

    font-weight: bold;

    background: white;

    box-shadow:
        0 2px 10px
        rgba(0,0,0,0.18);

    cursor: pointer;
}

</style>

</head>


<body>


<!-- ==================================
     NHẠC
================================== -->

<audio
    id="bgMusic"
    loop
    preload="auto"
>

    <source
        src="__MUSIC_DATA__"
        type="audio/mpeg"
    >

</audio>


<button
    id="musicButton"
    type="button"
>
    🔊 Bật nhạc
</button>


<!-- ==================================
     3 - 2 - 1
================================== -->

<div
    id="countScreen"
    class="screen active"
>

    <div id="count">
        3
    </div>

</div>


<!-- ==================================
     TRƯỜNG ĐUA
================================== -->

<div
    id="raceScreen"
    class="screen"
>

    <div class="title">
        🏁 TRƯỜNG ĐUA VỊT 🦆
    </div>

    <div id="raceList">
        __LANES__
    </div>

</div>


<!-- ==================================
     KẾT QUẢ
================================== -->

<div
    id="resultScreen"
    class="screen"
>

    <div id="resultBox">

        <h1>
            🏆 KẾT QUẢ CUỘC ĐUA 🏆
        </h1>

        <div id="ranking">
        </div>

    </div>

</div>


<script>


// ==================================
// DỮ LIỆU
// ==================================

const names = __NAMES__;

const speeds = __SPEEDS__;

const ducks = [];

const finishOrder = [];


// ==================================
// NHẠC
// ==================================

const bgMusic =
    document.getElementById(
        "bgMusic"
    );

const musicButton =
    document.getElementById(
        "musicButton"
    );


bgMusic.volume = 0.45;


function startMusic() {

    bgMusic
        .play()
        .then(() => {

            musicButton.style.display =
                "none";

        })
        .catch(() => {

            musicButton.style.display =
                "block";

        });

}


musicButton.addEventListener(
    "click",
    () => {

        bgMusic
            .play()
            .then(() => {

                musicButton.style.display =
                    "none";

            });

    }
);


// ==================================
// TẠO CÁC CON VỊT
// ==================================

for (
    let i = 0;
    i < names.length;
    i++
) {

    ducks.push({

        element:
            document.getElementById(
                "duck" + i
            ),

        position: 0,

        speed: speeds[i],

        finished: false

    });

}


// ==================================
// ĐỔI MÀN HÌNH
// ==================================

function showScreen(id) {

    document
        .querySelectorAll(
            ".screen"
        )
        .forEach(
            screen => {

                screen.classList.remove(
                    "active"
                );

            }
        );

    document
        .getElementById(id)
        .classList.add(
            "active"
        );

}


// ==================================
// COUNTDOWN
// ==================================

let number = 3;

const count =
    document.getElementById(
        "count"
    );


// Bắt đầu nhạc
startMusic();


const countdown =
    setInterval(
        () => {

            number--;


            if (
                number > 0
            ) {

                count.innerText =
                    number;


                count.style.animation =
                    "none";


                void count.offsetWidth;


                count.style.animation =
                    "countPop 0.8s ease";

            }


            else {

                clearInterval(
                    countdown
                );


                count.innerText =
                    "🦆💨";


                setTimeout(
                    () => {

                        showScreen(
                            "raceScreen"
                        );


                        setTimeout(
                            () => {

                                race();

                            },
                            150
                        );

                    },
                    500
                );

            }

        },
        1000
    );


// ==================================
// CUỘC ĐUA
// ==================================

function race() {

    let stillRunning =
        false;


    ducks.forEach(
        (duck, index) => {

            if (
                !duck.finished
            ) {

                stillRunning =
                    true;


                duck.position +=
                    duck.speed *
                    0.15;


                // Tăng tốc ngẫu nhiên

                if (
                    Math.random()
                    < 0.012
                ) {

                    duck.position +=
                        Math.random()
                        * 1.5;

                }


                // Về đích

                if (
                    duck.position >= 93
                ) {

                    duck.position =
                        93;

                    duck.finished =
                        true;

                    finishOrder.push(
                        index
                    );

                }


                duck.element.style.left =
                    duck.position +
                    "%";

            }

        }
    );


    if (
        stillRunning
    ) {

        requestAnimationFrame(
            race
        );

    }

    else {

        setTimeout(
            showResults,
            700
        );

    }

}


// ==================================
// HIỆN KẾT QUẢ
// ==================================

function showResults() {

    showScreen(
        "resultScreen"
    );


    const ranking =
        document.getElementById(
            "ranking"
        );


    ranking.innerHTML =
        "";


    const medals = [
        "🥇",
        "🥈",
        "🥉"
    ];


    finishOrder.forEach(
        (duckIndex, position) => {

            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "rank";


            if (
                position === 0
            ) {

                row.classList.add(
                    "first"
                );

            }


            const medal =
                position < 3
                ? medals[position]
                : "🏅";


            row.innerHTML =
                medal +
                " Hạng " +
                (position + 1) +
                " — 🦆 " +
                names[duckIndex];


            ranking.appendChild(
                row
            );

        }
    );


    createBalloons();

}


// ==================================
// BÓNG BAY
// ==================================

function createBalloons() {

    const items = [
        "🎈",
        "🎈",
        "🎈",
        "🫧",
        "🎉",
        "✨"
    ];


    for (
        let i = 0;
        i < 50;
        i++
    ) {

        setTimeout(
            () => {

                const balloon =
                    document.createElement(
                        "div"
                    );


                balloon.className =
                    "balloon";


                balloon.innerText =
                    items[
                        Math.floor(
                            Math.random()
                            * items.length
                        )
                    ];


                balloon.style.left =
                    Math.random() *
                    100 +
                    "%";


                balloon.style.animationDuration =
                    (
                        2.5 +
                        Math.random() *
                        2
                    ) +
                    "s";


                document.body.appendChild(
                    balloon
                );


                setTimeout(
                    () => {

                        balloon.remove();

                    },
                    5000
                );

            },
            i * 70
        );

    }

}

</script>


</body>

</html>
"""


        # ==================================
        # THAY DỮ LIỆU VÀO HTML
        #
        # Không dùng f-string
        # ==================================

        race_html = race_html.replace(
            "__MUSIC_DATA__",
            music_data
        )

        race_html = race_html.replace(
            "__LANES__",
            lanes
        )

        race_html = race_html.replace(
            "__NAMES__",
            names_js
        )

        race_html = race_html.replace(
            "__SPEEDS__",
            speeds_js
        )


        # ==================================
        # CHẠY TRÒ CHƠI
        # ==================================

        components.html(
            race_html,
            height=700,
            scrolling=False
        )

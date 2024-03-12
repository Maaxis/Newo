let skin = document.querySelector('link').href;
if (skin.includes("skin11") {
    var high_performance = true;
}

if (high_performance) { // do not run any code in High Performance
    let today = new Date();
    let hour = today.getHours();
    if (skin.includes("skin9") && hour < 21 && hour > 5) { // if skin is set to time switcher AND hour is between 6am and 9pm
        change_to_day(); // use day skin
    }
    else if (skin.includes("skin9")) { // if skin is set to time switcher but time is not between 6am-9pm
        change_to_night(); // use night skin
    }

    function change_to_day() {
        let link = document.querySelector('link');
        link.setAttribute("href", "/Forums/void5/skin7.css") // actually changes the skin
        skin = "skin7"; // change this variable from skin9 (time-switcher) to skin7 (day). does not change the visible skin for the user, but allows the skin variable to be reusable for later references to day-only functions
    }

    function change_to_night() {
        let link = document.querySelector('link');
        link.setAttribute("href", "/Forums/void5/skin8.css") // actually changes the skin
        skin = "skin8"; // change this variable from skin9 (time-switcher) to skin8 (night). does not change the visible skin for the user, but allows the skin variable to be reusable for later references to night-only functions
    }
} // closes if statement for High Performance check

if (!(skin.includes("skin11"))) { // do not run any code in High Performance
    // create petals in day skin
    var time_of_day = "";
    if (skin.includes("skin7")) {
        time_of_day = "Day";
    }
    else if (skin.includes("skin8")) {
        time_of_day = "Night";
    }
    function time_based_animations() {
        if (time_of_day == "Day") { // only run on day skin
            var petalImages = [
                "https://i.imgur.com/6Hh2ORr.png",
                "https://i.imgur.com/8FjLsrh.png",
                "https://i.imgur.com/J24RSs6.png",
                "https://i.imgur.com/w0CQfQH.png",
                "https://i.imgur.com/XZg32IB.png",
                "https://i.imgur.com/kfdF6yi.png",
                "https://i.imgur.com/EHWHhML.png"
            ];
            var startPos = ["bl", "tl", "br", "tr"];
            function createPetal() {
                var petal = document.createElement("div");
                var start = startPos[Math.floor(Math.random() * startPos.length)];
                var rand_index = Math.floor(Math.random() * petalImages.length);
                var rand_img_url = petalImages[rand_index];
                var img = document.createElement("img");
                petal.className = "petal";
                img.src = rand_img_url;
                if (start == "bl") {
                    petal.style.setProperty("--random-x", Math.random() * 25 + "vw");
                    petal.style.setProperty("--random-y", -Math.random() * 25 + "vh");
                    petal.style.bottom = "-20px";
                    petal.style.left = "-20px";
                } else if (start == "br") {
                    petal.style.setProperty("--random-x", -Math.random() * 25 + "vw");
                    petal.style.setProperty("--random-y", -Math.random() * 25 + "vh");
                    petal.style.bottom = "-20px";
                    petal.style.right = "-20px";
                } else if (start == "tr") {
                    petal.style.setProperty("--random-x", -Math.random() * 25 + "vw");
                    petal.style.setProperty("--random-y", Math.random() * 25 + "vh");
                    petal.style.top = "-20px";
                    petal.style.right = "-20px";
                } else {
                    petal.style.setProperty("--random-x", Math.random() * 25 + "vw");
                    petal.style.setProperty("--random-y", Math.random() * 25 + "vh");
                    petal.style.top = "-20px";
                    petal.style.left = "-20px";
                }
                petal.style.setProperty(
                    "--random-rotate-start",
                    Math.random() * 720 - 360 + "deg"
                );
                petal.style.setProperty(
                    "--random-rotate-end",
                    Math.random() * 720 - 360 + "deg"
                );
                petal.style.setProperty('--duration', (Math.random() * 5) + 5 + 's');
                var width = Math.random() * 10 + 10;
                img.style.width = width + "px";
                petal.addEventListener("animationend", function () {
                    document.body.removeChild(petal);
                });
                petal.appendChild(img);
                document.body.appendChild(petal);
            } //createPetal()
            setInterval(createPetal, 400);
        } // day skin check
        else if (time_of_day == "Night") {
            var fireflies = 15;
            var $container = $("<div class='container'></div>"); // Create a container element
            $("body").append($container); // Append it to the body element
            var $containerWidth = $container.width();
            var $containerHeight = $container.height();
            var master = new TimelineMax();
            for (var i = 0; i < fireflies; i++) {
                var firefly = $('<div class="firefly"></div>');
                TweenLite.set(firefly, {
                    x: Math.random() * $containerWidth,
                    y: Math.random() * $containerHeight
                });
                $container.append(firefly);
                fly(firefly);
            }
            function fly(elm) {
                var flyTl = new TimelineMax();
                var fadeTl = new TimelineMax({
                    delay: Math.floor(Math.random() * 2) + 1,
                    repeatDelay: Math.floor(Math.random() * 6) + 1,
                    repeat: -1
                });
                fadeTl.to(
                    [elm],
                    0.25,
                    { opacity: 0.25, yoyo: true, repeat: 1, repeatDelay: 0.2, yoyo: true },
                    Math.floor(Math.random() * 6) + 1
                );
                flyTl
                    .set(elm, { scale: Math.random() * 0.75 + 0.5 })
                    .to(elm, Math.random() * 100 + 100, {
                        bezier: {
                            values: [
                                {
                                    x: Math.random() * $containerWidth,
                                    y: Math.random() * $containerHeight
                                },
                                {
                                    x: Math.random() * $containerWidth,
                                    y: Math.random() * $containerHeight
                                }
                            ]
                        },
                        onComplete: fly,
                        onCompleteParams: [elm]
                    });
            } //fly()
        } //night skin check
    } //time_based_animations

    let shop_dialogue_blank = "https://i.imgur.com/kZTHNCV.png";
    let shop_dialogue_day = [
        "https://i.imgur.com/vqNTBgh.gif",
        "https://i.imgur.com/aZYXYVa.gif",
        "https://i.imgur.com/dNFLHaD.gif",
        "https://i.imgur.com/AACRDud.gif",
        "https://i.imgur.com/Y3nRTZI.gif",
        "https://i.imgur.com/Ony6rBS.gif",
        "https://i.imgur.com/ssunAWQ.gif"
    ];
    let shop_dialogue_night = [
        "https://i.imgur.com/hfJRjr6.gif",
        "https://i.imgur.com/TgsfHKJ.gif",
        "https://i.imgur.com/1fXMlH7.gif",
        "https://i.imgur.com/223oIzH.gif",
        "https://i.imgur.com/MDcjIp0.gif",
        "https://i.imgur.com/6f87mpZ.gif",
        "https://i.imgur.com/Ez4ylCP.gif"
    ];

    function shop_dialogue(blank_img) {
        var rand_index = Math.floor(Math.random() * 7);
        var rand_img_url = "";
        if (time_of_day == "Day") {
            var rand_img_url = shop_dialogue_day[rand_index];
        } else if (time_of_day == "Night") {
            var rand_img_url = shop_dialogue_night[rand_index];
        }
        blank_img.src = rand_img_url;
    }

    function swap_img() {
        var imgs = document.getElementsByTagName("img");
        for (var i = 0; i < imgs.length; i++) {
            for (const [key, value] of Object.entries(time_based_images)) {
                if ((imgs[i].src == key) && (time_of_day == "Night")) { // if skin is night and image is day
                    imgs[i].src = value; // switch image to night
                } else if ((imgs[i].src == value) && (time_of_day == "Day")) { // if skin is day and image is night
                    imgs[i].src = key; // switch image to day
                } else if ((imgs[i].src == shop_dialogue_blank)) {
                    shop_dialogue(imgs[i]);
                }
            }
        }
    }

    // script to change all images based on day/night
    // for each entry, make the first url the day version and the second url the night version.
    // comma is required after each entry except for the last one
    // only one entry per pair is required; any originally night image will switch to day at day and any originally day image will switch to night at night
    let time_based_images = {
        // "dayurl1.png": "nighturl1.png",
        // "dayurl2.png": "nighturl2.png",
        // "dayurl3.png": "nighturl3.png"
        // MEM WALL
        "https://i.imgur.com/AWOfv54.png": "https://i.imgur.com/dC4chVe.png", // Austen
        "https://i.imgur.com/cUQJCXZ.png": "https://i.imgur.com/xKC0Xih.png", // Blaire
        "https://i.imgur.com/WfH8URX.png": "https://i.imgur.com/sckgNb7.png", // Chloe
        "https://i.imgur.com/GNmIBFt.png": "https://i.imgur.com/iKtOKjK.png", // Emerson
        "https://i.imgur.com/Y02Graq.png": "https://i.imgur.com/v8GfXNF.png", // Franklin
        "https://i.imgur.com/1DZqwMi.png": "https://i.imgur.com/JrEdvGz.png", // Harvey
        "https://i.imgur.com/5u3ObLA.png": "https://i.imgur.com/X3pcfCy.png", // Indigo
        "https://i.imgur.com/lVQU5e7.png": "https://i.imgur.com/r7Ihiy1.png", // Justine
        "https://i.imgur.com/NVGYCMe.png": "https://i.imgur.com/yxG0iUR.png", // Katara
        "https://i.imgur.com/I74qU0V.png": "https://i.imgur.com/Pa6euex.png", // Landon
        "https://i.imgur.com/0UjJeWy.png": "https://i.imgur.com/XqUufrH.png", // Neil
        "https://i.imgur.com/hmBiI6f.png": "https://i.imgur.com/KpLYMqm.png", // Otis
        "https://i.imgur.com/93i2yJZ.png": "https://i.imgur.com/qvoyn4a.png", // Persephone
        "https://i.imgur.com/x32LkYq.png": "https://i.imgur.com/D1xzjIV.png", // Riley
        "https://i.imgur.com/jm2NQkI.png": "https://i.imgur.com/xcmo8Wa.png", // Tanner
        "https://i.imgur.com/ueb36LD.png": "https://i.imgur.com/LhzL1jS.png", // Victoria
        "https://i.imgur.com/VJR5wY3.png": "https://i.imgur.com/wSWcq16.png", // Winter
        "https://i.imgur.com/skTM6bm.png": "https://i.imgur.com/uRYIi6H.png", // Zelda
        // post marker
        "https://i.imgur.com/RXqTI54.png": "https://i.imgur.com/DXzDPxt.png",
        // AVATARS
        "https://i.imgur.com/9GgeAQ8.png": "https://i.imgur.com/YZzraW1.png", //Axel avatar
        "https://i.imgur.com/j0q8QiQ.png": "https://i.imgur.com/EDASDzj.png", //Saoirse avatar
        "https://i.imgur.com/eN5znBI.png": "https://i.imgur.com/oBgNtIJ.png", //Vivid avatar
        "https://i.imgur.com/BKvNDQv.png": "https://i.imgur.com/f4gsgt0.png", //Austen avatar
        "https://i.imgur.com/IyIHDsy.png": "https://i.imgur.com/3zOASGt.png", //Blaire avatar
        "https://i.imgur.com/m8UQomn.png": "https://i.imgur.com/WtLXPYg.png", //Chloe avatar
        "https://i.imgur.com/Nsg95Kk.png": "https://i.imgur.com/EgqruGt.png", //Emerson avatar
        "https://i.imgur.com/YhIio0Z.png": "https://i.imgur.com/EPbhrRY.png", //Franklin avatar
        "https://i.imgur.com/gqPeLqu.png": "https://i.imgur.com/mtlplqT.png", //Harvey avatar
        "https://i.imgur.com/itMr3Uy.png": "https://i.imgur.com/KlkpIVc.png", //Indigo avatar
        "https://i.imgur.com/9warB5r.png": "https://i.imgur.com/fwwlxc1.png", //Justine avatar
        "https://i.imgur.com/JHXuq5I.png": "https://i.imgur.com/1kapvMJ.png", //Katara avatar
        "https://i.imgur.com/VT1xGDb.png": "https://i.imgur.com/Eud3ldm.png", //Landon avatar
        "https://i.imgur.com/Bo6Z0K1.png": "https://i.imgur.com/YMVFArE.png", //Neil avatar
        "https://i.imgur.com/wqNqs4f.png": "https://i.imgur.com/fortgAs.png", //Otis avatar
        "https://i.imgur.com/2cTLEBW.png": "https://i.imgur.com/5CZjqUz.png", //Persephone avatar
        "https://i.imgur.com/n0eEcSd.png": "https://i.imgur.com/Io7mYnp.png", //Riley avatar
        "https://i.imgur.com/7CjtJ8A.png": "https://i.imgur.com/dPIOIgM.png", //Tanner avatar
        "https://i.imgur.com/Ju6bnNH.png": "https://i.imgur.com/CQjaK6o.png", //Victoria avatar
        "https://i.imgur.com/9HAysZn.png": "https://i.imgur.com/2BHFUsc.png", //Winter avatar
        "https://i.imgur.com/Lo51tXx.png": "https://i.imgur.com/AJ0eLvj.png", //Zelda avatar
        "https://i.imgur.com/0Rcgn9t.png": "https://i.imgur.com/h7qnow4.png", //Quinn avatar
        "https://i.imgur.com/HH65GlL.png": "https://i.imgur.com/Wyg0JUm.png", //Gabriel avatar
        "https://i.imgur.com/yViSmZ7.png": "https://i.imgur.com/UbmVWfF.png", //Cypress avatar
        "https://i.imgur.com/B8rmRcq.png": "https://i.imgur.com/IqZH3ks.png", //Calliope avatar
        "https://i.imgur.com/Xa2I9Oh.png": "https://i.imgur.com/O33ZRq2.png", //Phoenix avatar
        "https://i.imgur.com/jtAQEsC.png": "https://i.imgur.com/vQQr4th.png", //Niamh avatar
        "https://i.imgur.com/bvwJ0jL.png": "https://i.imgur.com/jmm73ip.png", //Piper avatar
        "https://i.imgur.com/Ihj2CRj.png": "https://i.imgur.com/AvvKfeN.png", //Viola avatar
        "https://i.imgur.com/8cfkBiz.png": "https://i.imgur.com/ArF03th.png", //Luca avatar
        "https://i.imgur.com/MIFQhxD.png": "https://i.imgur.com/qI13nQM.png", //Juno avatar
        //CHALLENGE BANNERS
        "https://i.imgur.com/1T5e3Hu.png": "https://i.imgur.com/vtOTpvT.png", //Intro to Floriculture
    };

    window.onload = function start() {
        time_based_animations();
        swap_img();
    };
}
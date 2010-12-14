({
    appDir: "../static",
    baseUrl: "js",
    dir: "../static_build",
    optimizeCss: "standard",
    modules: [
        {
            name: "pages/base",
            exclude: ["jquery"],
            include: ["libs/webfont", "libs/jquery.ui", "libs/jquery.form", "mods/feedback", "mods/messages", "mods/facebook", "pages/base"]
        },
        {
            name: "pages/rah.home_logged_out",
            exclude: ["jquery", "pages/base"],
            include: ["libs/jquery.cookie", "mods/pledge"]
        }
    ]
})

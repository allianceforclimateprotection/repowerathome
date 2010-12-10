({
    appDir: "../static",
    baseUrl: "js",
    dir: "../static_build",
    modules: [
        {
            name: "common",
            create: true,
            exclude: ["jquery"],
            include: ["libs/webfont", "libs/jquery.ui", "libs/jquery.form", "mods/feedback", "mods/messages", "mods/facebook"]
        },
        {
            name: "pages/rah.home_logged_out",
            exclude: ["jquery", "common"],
            include: ["libs/jquery.cookie", "mods/pledge"]
        }
    ]
})


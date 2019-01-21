// Original From: https://imjad.cn/archives/lab/add-dynamic-poster-girl-with-live2d-to-your-blog-02
// Original From: https://www.fghrsh.net/post/123.html

// Rewrite By LXG_Shadow

var tipsTimeout = "";

function waifu() {

    // waifu 设置
    this.waifuSize = null; // 模型 width height
    this.waifuMinWidth = null; //单位px
    this.waifuEdgeSide = null;
    this.waifuDraggable = null;
    this.waifuDraggableRevert = null; // 松开鼠标还原拖拽位置

    // 模型
    this.model = new Object;
    this.model.ChangeApi = null;
    this.model.GetApi = null;
    this.model.Url = null;
    this.model.Id = null;
    this.model.TextureId = null;
    this.model.Name = null;

    //设置
    this.setting = new Object;
    this.setting.showConsoleLogs = null; // 显示控制台信息
    this.setting.enableTips = null;
    this.setting.enableToolbar = null;
    this.setting.enableHitokoto = null; // 一言

    // 提示消息设置
    this.tips = new Object;
    this.tips.Url = null;
    this.tips.ShowingPeriod = null; //消息停留时间 (ms)
    this.tips.FadeTime = null; // 消息 消失/出现 速度 (ms)
    this.tips.Size = null;
    this.tips.Top = null;
    this.tips.FontSize = null;
    this.tips.showWelcomeMessage = null;
    this.tips.showSiteInfo = null;
    this.tips.showCopyMessage = null;

    // 一言设置
    this.hitokoto = new Object;
    this.hitokoto.Api = null;
    this.hitokoto.Cat = null;
    this.hitokoto.Encoding = null;
    this.hitokoto.Charset = null;
    this.hitokoto.ShowingPeriod = null;


    // toolbar 设置
    this.toolbar = new Object;
    //this.toolbar.

    this.initWaifu = function () {
        this.loadWaifu();
        if (this.setting.enableTips) this.loadWaifuTips();
        if (this.setting.enableToolbar) this.loadWaifuToolbar();
        if (this.setting.enableHitokoto) window.setInterval(function (waifu) {
            waifu.showHitokoto();
        }, this.hitokoto.ShowingPeriod, this);
        this.printConsoleLog("waifu初始化成功");
    };

    this.initWaifuFromConfig = function (url) {
        var waifu = this;
        $.ajax({
            cache: true,
            url: url,
            dataType: "json",
            success: function (result) {
                if (result["code"] === "1") {
                    waifu.waifuSize = result["data"].waifuSize;
                    waifu.waifuMinWidth = result["data"].waifuMinWidth;
                    waifu.waifuEdgeSide = result["data"].waifuEdgeSide;
                    waifu.waifuDraggable = result["data"].waifuDraggable;
                    waifu.waifuDraggableRevert = result["data"].waifuDraggableRevert;
                    waifu.model = result["data"].model;
                    waifu.setting = result["data"].setting;
                    waifu.tips = result["data"].tips;
                    waifu.hitokoto = result["data"].hitokoto;
                    waifu.initWaifu();
                }
            }
        });
    };

    this.loadWaifu = function () {
        var waifu = this;

        $("#live2d").prop("width", this.waifuSize[0]);
        $("#live2d").prop("height", this.waifuSize[1]);

        loadlive2d("live2d", this.model.Url);

        $("#waifu").css(this.waifuEdgeSide.split(":")[0], this.waifuEdgeSide.split(":")[1]);
        $("#waifu").draggable({"disabled": !this.waifuDraggable, "revert": this.waifuDraggableRevert});
        if ($(window).width() <= waifu.waifuMinWidth) $("#waifu").hide();
        $(window).resize(function () {
            if ($(window).width() <= waifu.waifuMinWidth) {
                $("#waifu").hide();
            } else {
                $("#waifu").show();
            }
        });

        this.printConsoleLog("模型加载完成");
    };

    this.loadWaifuTips = function () {
        $("#waifu-tips").css("top", this.tips.Top);
        $(".waifu-tips").css("font-size", this.tips.FontSize);
        $(".waifu-tips").width(this.tips.Size[0]);
        $(".waifu-tips").height(this.tips.Size[1]);
        var waifu = this;
        $.ajax({
            cache: true,
            url: waifu.tips.Url,
            dataType: "json",
            success: function (result) {
                $.each(result.mouseover, function (index, tips) {
                    $(document).on("mouseover", tips.selector, function () {
                        var text = tips.text;
                        if (Array.isArray(tips.text)) text = tips.text[Math.floor(Math.random() * tips.text.length + 1) - 1];
                        waifu.showMessage(text, null);
                    });
                });
                $.each(result.click, function (index, tips) {
                    $(document).on("click", tips.selector, function () {
                        var text = tips.text;
                        if (Array.isArray(tips.text)) text = tips.text[Math.floor(Math.random() * tips.text.length + 1) - 1];
                        waifu.showMessage(text, null);
                    });
                });

                if (waifu.tips.showCopyMessage) {
                    $(document).on('copy', function () {
                        waifu.showMessage(result.tips.copy, null);
                    });
                }
            }
        });

        this.printConsoleLog("加载提示完成");
    };

    this.loadWaifuToolbar = function () {
        var waifu = this;
        $(".waifu-tool .glyphicon-picture").click(function () {
            waifu.takePhoto();
        });
        $(".waifu-tool .glyphicon-refresh").click(function () {
            waifu.changeModel();
        });
        $(".waifu-tool .glyphicon-eye-open").click(function () {
            waifu.changeTexture();
        });
        $(".waifu-tool .glyphicon-remove").click(function () {
            localStorage.setItem("enableWaifu","0");
            $("#waifu").empty();
            $("#open-waifu").show();
        });
        $(".waifu-tool .glyphicon-book").click(function () {
            waifu.showHitokoto();
        });
        $(".waifu-tool .glyphicon-info-sign").click(function () {
            waifu.showMessage("我是" + waifu.model.Name + " 是本网站的看板娘哦！", null);
        });
        $(".waifu-tool .glyphicon-home").click(function () {
            window.location.href = "/";
        });
    };

    this.takePhoto = function () {
        window.Live2D.captureFrame = true;

        this.printConsoleLog("人物截图以保存");
    };

    this.changeModel = function () {
        var waifu = this;
        $.ajax({
            cache: true,
            url: waifu.model.ChangeApi + "?cm=1&id=" + waifu.model.Id + "&tid=" + waifu.model.TextureId,
            dataType: "json",
            success: function (result) {
                if (result["code"] === "1") {
                    waifu.model.Id = result["data"].Id;
                    waifu.model.Name = result["data"].Name;
                    waifu.model.TextureId = result["data"].TextureId;
                    waifu.model.Url = waifu.model.GetApi + "?id=" + waifu.model.Id + "&tid=" + waifu.model.TextureId;
                    waifu.loadWaifu();
                }
            }
        });
        this.printConsoleLog("更换人物成功");
    };

    this.changeTexture = function () {
        var waifu = this;
        $.ajax({
            cache: true,
            url: waifu.model.ChangeApi + "?ct=1&id=" + waifu.model.Id + "&tid=" + waifu.model.TextureId,
            dataType: "json",
            success: function (result) {
                if (result["code"] === "1") {
                    waifu.model.Id = result["data"].Id;
                    waifu.model.Name = result["data"].Name;
                    waifu.model.TextureId = result["data"].TextureId;
                    waifu.model.Url = waifu.model.GetApi + "?id=" + waifu.model.Id + "&tid=" + waifu.model.TextureId;
                    waifu.loadWaifu();
                }
            }
        });
        this.printConsoleLog("更换服装成功");
    };

    this.showHitokoto = function () {
        var waifu = this;
        var cat = waifu.hitokoto.Cat[Math.floor(Math.random() * waifu.hitokoto.Cat.length + 1) - 1];
        $.ajax({
            cache: true,
            url: waifu.hitokoto.Api + "?c=" + cat + "&encode=" + waifu.hitokoto.Encoding + "&charset=" + waifu.hitokoto.Charset,
            dataType: "json",
            success: function (result) {
                if (typeof (result.status) == "undefined") {
                    var temp = "     --";
                    waifu.showMessage(result["hitokoto"] + temp + result["from"], null);
                }
            }
        });
    };

    this.showMessage = function (text, timeout) {
        clearTimeout(tipsTimeout);
        this.hideMessage(0);
        if (timeout === null) timeout = this.tips.ShowingPeriod;
        if (Array.isArray(text)) text = text[Math.floor(Math.random() * text.length + 1) - 1]; // 如果 text为list 随机取一句话
        $('.waifu-tips').stop(); // 停止 jquery动画
        $('.waifu-tips').html(text).fadeTo(this.tips.FadeTime, 1);
        tipsTimeout = setTimeout(this.hideMessage, timeout, this.tips.MessageFadeTime);

        this.printConsoleLog("显示消息: " + text);
    };


    this.hideMessage = function (MessageFadeTime) {
        $('.waifu-tips').stop();
        $('.waifu-tips').fadeTo(MessageFadeTime, 0);
    };

    this.printConsoleLog = function (text) {
        if (!this.setting.showConsoleLogs) return;
        console.log(text);
    };

}
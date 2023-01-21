var main = (function($) { var _ = {
    $window: null,

    $postList: null,

    $waitingCount: 0,

    $currentIndex: 0,

    $toTakeCount: 10,

    startup: function() {
        _.$window = $(window);

        // waiting for fetch and for load
        _.$waitingCount = 2;

        fetch("/assets/js/scraped.json")
            .then((response) => response.json())
            .then((json) => {
                _.$postList = json.entries.reverse();
                if (--_.$waitingCount === 0) {
                    _.initialize();
                }
            })

        _.$window.on('load', function() {
            if (--_.$waitingCount === 0) {
                _.initialize();
            }
        });
    },

    initialize: function() {
        // horizontal
        //_.setFocus("https://com-jameskeats-photo.s3.amazonaws.com/2023-01-xx/DSC_0609_thumb.jpg", "https://com-jameskeats-photo.s3.amazonaws.com/2023-01-xx/DSC_0609.jpg")

        // vertical
        //_.setFocus("https://com-jameskeats-photo.s3.amazonaws.com/2022-09-XX/DSC_0409_thumb.jpg", "https://com-jameskeats-photo.s3.amazonaws.com/2022-09-XX/DSC_0409.jpg")

        $("#leftbutton").click(function() {
            _.pageLeft();
        })

        $("#rightbutton").click(function() {
            _.pageRight();
        })

        let chosenEntry = _.$postList[Math.floor(Math.random() * _.$postList.length)];
        _.setFocus(chosenEntry.thumb, chosenEntry.fullsize);
        _.validateTakeCount();
        _.setupGallery();

        $(window).resize(function () { _.handleResize(); });
    },

    handleResize: function() {
        const oldValue = _.$toTakeCount;
        _.validateTakeCount();
        if (_.$toTakeCount !== oldValue)
        {
            _.setupGallery();
        }
    },

    validateTakeCount: function() {
        const sm = "(min-width: 720px)";
        const md = "(min-width: 1180px)";
        const lg = "(min-width: 1380px)";
        const xl = "(min-width: 1520px)";

        const oldValue = _.$toTakeCount;
        if (window.matchMedia(xl).matches || window.matchMedia(lg).matches)
        {
            console.log("we think we're big")
            _.$toTakeCount = 10;
        }
        else if (window.matchMedia(md).matches || window.matchMedia(sm).matches)
        {
            console.log("we think we're md")
            _.$toTakeCount = 4;
        }
        else
        {
            console.log("we think we're sm")
            _.$toTakeCount = 6;
        }

        return _.$toTakeCount !== oldValue;
    },

    setFocus: function(thumbUrl, bigUrl) {
        //$("#bg").attr("src", thumbUrl);
        $("#backdrop").css("background-image", "url(\"" + thumbUrl + "\")");
        $("#showcase").attr("src", thumbUrl);
        $("#clickme").attr("href", bigUrl);
    },

    pageLeft: function() {
        _.$currentIndex -= _.$toTakeCount
        _.setupGallery();
    },

    pageRight: function() {
        _.$currentIndex += _.$toTakeCount
        _.setupGallery();
    },

    setupGallery: function() {
        let gallery = $("#gallery");
        gallery.empty();

        const toTake = _.$toTakeCount;
        _.$currentIndex = Math.min(_.$postList.length - toTake, _.$currentIndex);
        _.$currentIndex = Math.max(_.$currentIndex, 0);

        const start = _.$currentIndex;
        const end = Math.min(start + toTake, _.$postList.length);
        for (let i = start; i < end; ++i) {
            const thisEntry = _.$postList[i];
            gallery.append(
                `<button id="gallery-${i}"><img class="rounded-lg object-cover w-56 h-32 m-2" src="${thisEntry.thumb}"></img></button>`
            )

            $(`#gallery-${i}`).click(function() {
                _.setFocus(thisEntry.thumb, thisEntry.fullsize);
            })
        }
    }

}; return _; })(jQuery); main.startup();

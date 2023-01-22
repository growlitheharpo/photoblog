var main = (function($) { var _ = {
    $window: null,

    $postList: null,

    $waitingCount: 0,

    $currentIndex: 0,

    $toTakeCount: 10,

    $selectedItem: null,

    $selectedClasses: "border-solid border-orange-400 border-4",

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

        const chosenEntry = _.$postList[Math.floor(Math.random() * _.$postList.length)];
        _.validateTakeCount();
        _.setupGallery();
        _.setFocus(chosenEntry);

        $(window).resize(function () { _.handleResize(); });
    },

    handleResize: function() {
        if (_.validateTakeCount())
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
        const gallery = $("#gallery");
        const galleryHeight = gallery.height();
        const itemHeight = 128; // todo: don't hardcode this??
        const maxVertical = Math.floor(galleryHeight / (itemHeight * 1.08));

        if (window.matchMedia(xl).matches || window.matchMedia(lg).matches)
        {
            // For the large layout, we have 2 columns
            _.$toTakeCount = maxVertical * 2;
        }
        else if (window.matchMedia(md).matches || window.matchMedia(sm).matches)
        {
            _.$toTakeCount = maxVertical;
        }
        else
        {
            _.$toTakeCount = 6;
        }

        return _.$toTakeCount !== oldValue;
    },

    setFocus: function(newTarget) {
        const previousTargetIndex = _.$postList.indexOf(_.$selectedItem);
        const previousTargetElement = $(`#gallery-${previousTargetIndex}-image`);
        if (previousTargetElement) {
            previousTargetElement.removeClass(_.$selectedClasses);
        }

        _.$selectedItem = newTarget;
        $("#backdrop").css("background-image", "url(\"" + newTarget.thumb + "\")");
        $("#showcase").attr("src", newTarget.thumb);
        $("#clickme").attr("href", newTarget.fullsize);

        const targetIndex = _.$postList.indexOf(newTarget);
        const targetElement = $(`#gallery-${targetIndex}-image`);
        if (targetElement) {
            targetElement.addClass(_.$selectedClasses);
        }
    },

    determinePageCount: function() {
        return Math.ceil(_.$postList.length / _.$toTakeCount);
    },

    determineCurrentPage: function() {
        return Math.floor(_.$currentIndex / _.$toTakeCount) + 1;
    },

    pageLeft: function() {
        _.$currentIndex -= _.$toTakeCount;
        _.setupGallery();
    },

    pageRight: function() {
        _.$currentIndex += _.$toTakeCount;
        _.setupGallery();
    },

    setupGallery: function() {
        let gallery = $("#gallery");
        gallery.empty();

        const toTake = _.$toTakeCount;
        const pageCount = _.determinePageCount();

        const minValue = 0;
        const maxValue = (pageCount - 1) * toTake;
        _.$currentIndex = Math.max(Math.min(_.$currentIndex, maxValue), minValue);
        const currPage = _.determineCurrentPage();

        const start = _.$currentIndex;
        const end = Math.min(start + toTake, _.$postList.length);
        for (let i = start; i < end; ++i) {
            const thisEntry = _.$postList[i];
            gallery.append(
                `<button id="gallery-${i}">
                    <img class="rounded-lg object-cover w-56 h-32" src="${thisEntry.thumb}" id="gallery-${i}-image"></img>
                </button>`
            )

            const button = $(`#gallery-${i}`);
            button.click(function() {
                _.setFocus(thisEntry);
            })

            if (thisEntry === _.$selectedItem) {
                $(`gallery-${i}-image`).addClass(_.$selectedClasses);
            }
        }

        $("#pagecount").text(`${currPage} / ${pageCount}`);
    }

}; return _; })(jQuery); main.startup();

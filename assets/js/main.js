var main = (function ($) {
    var _ = {
        $window: null,

        $postList: null,

        $waitingCount: 0,

        $currentIndex: 0,

        $toTakeCount: 10,

        $selectedItem: null,

        $selectedClasses: "border-orange-400",

        $showcaseInfobox: null,

        $showcaseInfoEnableButton: null,

        $showcaseInfoDisableButton: null,

        startup: function () {
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

            _.$window.on('load', function () {
                if (--_.$waitingCount === 0) {
                    _.initialize();
                }
            });
        },

        initialize: function () {
            _.$showcaseInfoEnableButton = $("#showcase-infobox-on");
            _.$showcaseInfoDisableButton = $("#showcase-infobox-off");
            _.$showcaseInfobox = $("#showcase-infobox");

            _.$showcaseInfoEnableButton.click(function () {
                _.enableShowcaseInfo();
            });

            _.$showcaseInfoDisableButton.click(function () {
                _.disableShowcaseInfo();
            });

            $("#showcase-left").click(function () {
                _.showcaseLeft();
            });

            $("#showcase-right").click(function () {
                _.showcaseRight();
            });

            $("#gallery-left-button").click(function () {
                _.pageLeft();
            });

            $("#gallery-right-button").click(function () {
                _.pageRight();
            });

            $(document).keydown(function (e) {
                if (e.which === 37) {
                    _.showcaseLeft();
                }
                else if (e.which === 39) {
                    _.showcaseRight();
                }
                else if (e.which === 38) {
                    _.pageLeft();
                }
                else if (e.which === 40) {
                    _.pageRight();
                }
            });

            _.enableShowcaseInfo();

            const chosenEntry = _.$postList[0];
            _.validateTakeCount();
            _.setupGallery();
            _.setFocus(chosenEntry);

            $(window).resize(function () { _.handleResize(); });
        },

        handleResize: function () {
            if (_.validateTakeCount()) {
                _.setupGallery();
            }
        },

        validateTakeCount: function () {
            const oldValue = _.$toTakeCount;

            const sm = "(min-width: 720px)";
            const md = "(min-width: 1180px)";
            const lg = "(min-width: 1380px)";
            const xl = "(min-width: 1520px)";

            const screenHeight = $("#showcase-panel").height();
            const headerHeight = $("#gallery-header").height();
            const desiredHeight = screenHeight - headerHeight;
            const itemHeight = 155; //todo: don't hardcode this?
            const maxVertical = Math.max(Math.floor(desiredHeight / itemHeight), 1);

            if (window.matchMedia(xl).matches || window.matchMedia(lg).matches) {
                // For the large layout, we have 2 columns
                _.$toTakeCount = maxVertical * 2;
            }
            else if (window.matchMedia(md).matches || window.matchMedia(sm).matches) {
                _.$toTakeCount = maxVertical;
            }
            else {
                _.$toTakeCount = 6;
            }

            return _.$toTakeCount !== oldValue;
        },

        showcaseLeft: function () {
            const previousTargetIndex = _.$postList.indexOf(_.$selectedItem);
            const newIndex = Math.min(Math.max(previousTargetIndex - 1, 0), _.$postList.length - 1);
            const newEntry = _.$postList[newIndex];
            this.setFocus(newEntry);
        },

        showcaseRight: function () {
            const previousTargetIndex = _.$postList.indexOf(_.$selectedItem);
            const newIndex = Math.min(Math.max(previousTargetIndex + 1, 0), _.$postList.length - 1);
            const newEntry = _.$postList[newIndex];
            this.setFocus(newEntry);
        },

        setFocus: function (newTarget) {
            _.$selectedItem = newTarget;
            $("#backdrop").css("background-image", "url(\"" + newTarget.thumb + "\")");
            $("#showcase").attr("src", newTarget.thumb);
            $("#clickme").attr("href", newTarget.fullsize);
            $("#showcase-title").text(newTarget.title);
            $("#showcase-date").text((new Date(newTarget.date)).toDateString());

            const newPage = _.getPageForEntry(newTarget);
            const scrolled = _.scrollToPage(newPage);

            if (!scrolled) {
                _.handleSelectionHighlight();
            }

            _.handleShowcaseButtonVisibility();
        },

        determinePageCount: function () {
            return Math.ceil(_.$postList.length / _.$toTakeCount);
        },

        determineCurrentPage: function () {
            return Math.floor(_.$currentIndex / _.$toTakeCount) + 1;
        },

        getPageForEntry: function (entry) {
            const entryIndex = _.$postList.indexOf(entry);
            return Math.floor(entryIndex / _.$toTakeCount) + 1;
        },

        pageLeft: function () {
            _.$currentIndex -= _.$toTakeCount;
            _.setupGallery();
        },

        pageRight: function () {
            _.$currentIndex += _.$toTakeCount;
            _.setupGallery();
        },

        scrollToPage: function (targetPage) {
            const newIndex = (targetPage - 1) * _.$toTakeCount;
            if (_.$currentIndex !== newIndex) {
                _.$currentIndex = newIndex;
                _.setupGallery();
                return true;
            }

            return false;
        },

        setupGallery: function () {
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
                        <img id="gallery-${i}-image" class="rounded-lg object-cover w-56 h-32 border-4 border-solid" src="${thisEntry.thumb}">
                    </button>`
                )

                const button = $(`#gallery-${i}`);
                button.click(function () {
                    _.setFocus(thisEntry);
                })
            }

            _.handleSelectionHighlight();
            _.handleGalleryButtonVisibility();

            $("#page-count").text(`${currPage} / ${pageCount}`);
        },

        handleSelectionHighlight: function () {
            const children = $("#gallery>button>img");
            children.removeClass("border-orange-400");
            children.removeClass("border-transparent");
            children.addClass("border-transparent");

            const targetIndex = _.$postList.indexOf(_.$selectedItem);
            const targetElement = $(`#gallery-${targetIndex}-image`);
            if (targetElement) {
                targetElement.removeClass("border-transparent");
                targetElement.addClass("border-orange-400");
            }
        },

        handleShowcaseButtonVisibility: function () {
            const leftIcon = $("#showcase-left-icon");
            const rightIcon = $("#showcase-right-icon");
            leftIcon.removeClass("text-transparent").removeClass("text-white");
            rightIcon.removeClass("text-transparent").removeClass("text-white");

            const newIndex = _.$postList.indexOf(_.$selectedItem);
            if (newIndex <= 0) {
                leftIcon.addClass("text-transparent");
            } else {
                leftIcon.addClass("text-white");
            }

            if (newIndex >= _.$postList.length - 1) {
                rightIcon.addClass("text-transparent");
            } else {
                rightIcon.addClass("text-white");
            }
        },

        handleGalleryButtonVisibility: function () {
            const leftIcon = $("#gallery-left-button-icon");
            const rightIcon = $("#gallery-right-button-icon");
            leftIcon.removeClass("text-gray-300");
            rightIcon.removeClass("text-gray-300");

            const page = _.determineCurrentPage();
            const pageCount = _.determinePageCount();
            if (page === 1) {
                leftIcon.addClass("text-gray-300");
            }

            if (page === pageCount) {
                rightIcon.addClass("text-gray-300");
            }
        },

        enableShowcaseInfo: function () {
            _.$showcaseInfobox.removeClass("hidden");
            _.$showcaseInfoEnableButton.addClass("hidden");
        },

        disableShowcaseInfo: function () {
            _.$showcaseInfoEnableButton.removeClass("hidden");
            _.$showcaseInfobox.addClass("hidden");
        },

    }; return _;
})(jQuery); main.startup();

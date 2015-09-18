
    var stateEnabled = false,
        editFormBase = null;

    function toggleEditMode() {
        // Set editformbase element
        editFormBase = $(".editform");

        if (stateEnabled == true) {
            disableEditMode();
        } else {
            enableEditMode();
        }
    }

    function enableEditMode() {
        editFormBase.find(".editmode-form").css({"display": "block"});
        editFormBase.find(".editmode-labels").css({"display": "none"});
        stateEnabled = true;
    }

    function disableEditMode() {
        editFormBase.find(".editmode-form").css({"display": "none"});
        editFormBase.find(".editmode-labels").css({"display": "block"});
        stateEnabled = false;
    }

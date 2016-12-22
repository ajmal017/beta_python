$(function () {
    "use strict";

    var form = $("#pricing-plans"),
        inputSubmit = form.find("input[name=submit]");

    form
        .find(":submit").click(function () {
        inputSubmit.val($(this).data('type'));
    })
        .filter(".delete").click(function () {
        $(this).siblings("[name$='-DELETE']").prop('checked', true);
    });
    form.find("[name$='-person']").change(function () {
        var $this = $(this),
            parentId = $this.siblings(".form-parent").val(),
            input = $this.siblings(":hidden[name$='-parent']");
        if ($.isNumeric($this.val())) {
            input.val(parentId);
        } else {
            input.val("");
        }
    });
});

$(function () {
    betasmartz.widgets.searchTable("table.goals", undefined, {
        "initialSorting": []
    });

    $("table.goals tbody tr").find(".save-portfolio")
        .click(function () {
            var form = $(this).closest("form");
            $.post(location.href, {
                "csrfmiddlewaretoken": form.find("[name=csrfmiddlewaretoken]").val(),
                "object_pk": form.find("[name=object_pk]").val(),
                "goal_id": form.find("[name=goal_id]").val(),
                "portfolio_id": form.find("[name=portfolio_id] option:selected").val()
            }, function (r) {
                form.find(".save-portfolio").hide();
            });
        })
        .end()
        .find("select").change(function (e) {
        var select = $(e.currentTarget),
            submit = select.closest("tr").find(".save-portfolio");
        submit.toggleClass("hidden",
            select.find("option:selected").val() == select.data("originalValue"));
    });
});

$(document).ready(function () {
  $("form").submit(function (event) {
    event.preventDefault();

    radioChecked = $(this).find("input[name=choice]:checked").val();
    csrftoken = $(this).find("[name=csrfmiddlewaretoken]").val();
    answerId = $(this).find(".text-answer").attr("id");

    if (typeof radioChecked === "undefined") {
      $("#" + answerId)
        .html(
          "<p class='p-3 mb-3 bg-danger text-white'>Please, select an option.</p>"
        )
        .hide()
        .fadeIn("slow");
      return;
    }

    $.ajax({
      url: "",
      type: "post",
      beforeSend: function (request) {
        request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      data: {
        choice: radioChecked,
        question_id: this.id,
      },
      success: function (response) {
        $("#" + answerId).html(
          "<p class='p-3 mb-3 bg-primary text-white'>" +
            response.answer +
            "</p>"
        );
        if (response.is_answer == true) {
          $("#" + answerId)
            .append(
              "<p class='p-3 mb-3 bg-success text-white'>Your answer was correct. 😊</p>"
            )
            .hide()
            .fadeIn("slow");
        } else {
          $("#" + answerId)
            .append(
              "<p class='p-3 mb-3 bg-danger text-white'>Your answer was wrong. 😢</p>"
            )
            .hide()
            .fadeIn("slow");
        }
        // $('#'+answerId).css("visibility", "visible")
      },
    }).fail(function (jqXHR, exception) {
      let msg = "";
      if (jqXHR.status === 0) {
        msg = "Could not connect.\n Verify Network Connection";
      } else if (jqXHR.status == 404) {
        msg = "Requested page not found. [404]";
      } else if (jqXHR.status == 500) {
        msg = "Internal Server Error [500].";
      } else if (exception === "parsererror") {
        msg = "Requested JSON parse failed.";
      } else if (exception === "timeout") {
        msg = "Time out error.";
      } else if (exception === "abort") {
        msg = "Ajax request aborted.";
      } else {
        msg = "Uncaught Error.\n" + jqXHR.responseText;
      }
      $("#" + answerId).html(
        "<p class='p-3 mb-3 bg-danger text-white'>" + msg + "</p>"
      );
    });
  });

});

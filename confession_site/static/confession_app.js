$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $('.edit-button').click(function() {
      var confession_id = $(this).data('confession-id')
      var confession_text = $(this).data('confession-text')
      var user_session = $(this).data('session')
      event.preventDefault();
      event.stopPropagation();
      confession_text = prompt("Edit confession", confession_text)
      edit_post(confession_id, confession_text, user_session);
    });
    $('.contact-button').click(function(){
        event.preventDefault();
        event.stopPropagation();
        name = document.getElementById('id_name').value;
        email = document.getElementById('id_email').value;
        content = document.getElementById('id_contact_text').value;
        if (name === '' || email === '' || content === '')
        {
            alert("Please enter all the field to submit");
        }
        submit_contact(name, email, content);
    });
});


function validateForm_content() {
    let content = document.forms["confess_form"]["confess_content"].value;
    if (content==="" || content==="Your Confession goes here") {
        alert("Please input something to submit the confession");
        return false;
    }
}

function edit_post(confession_id, confession_text, user_session) {
  $.ajax({
    url: "/edit_post/",
    type: "POST",
    data: { id : confession_id, confession_edit : confession_text, user: user_session},

    success: function(json) {
      $("#talk").replaceWith("<p>" + json.edit + "</p>")
    },

    error: function(xhr,errmsg,err) {
      alert(xhr.status + ": " + xhr.responseText);
    }
  })
}

function submit_contact(name, email, content) {
    console.log(content)
    $.ajax({
        url: "/about/",
        type: "POST",
        data: { name: name, email: email, content: content},

        success: function(json) {
            $("div.contact-form-container").replaceWith("<h6 style=\"color:black;\">Your Contact Form Has Been Sent!</h6>");
            console.log(json.result)
        },

        error: function(xhr,errmsg,err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    })
}

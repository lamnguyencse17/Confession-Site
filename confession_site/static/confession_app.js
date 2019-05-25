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
      confession_text = prompt("Edit confession", confession_text);
      edit_post(confession_id, confession_text, user_session);
    });
    $('.delete-button').click(function() {
      var confession_id = $(this).data('confession-id')
      event.preventDefault();
      event.stopPropagation();
      delete_post(confession_id);
    })

    $('#scroll').scroll( function(){
      if (Math.abs($('#scroll').scrollTop() - ($('#scroll')[0].scrollHeight-$('#scroll').height())) <= 1)
      {
        scroll_position = $('#scroll').scrollTop()
        var page = $(this).data('page')
        console.log(page)
        load_post(page+1, scroll_position)
      }
    })
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
    url: "/edit_post",
    type: "POST",
    data: { id : confession_id, confession_edit : confession_text, user: user_session},

    success: function(json) {
      $('#'+confession_id).replaceWith("<p>" + json.edit + "</p>")
    },

    error: function(xhr,errmsg,err) {
      alert(xhr.status + ": " + xhr.responseText);
    }
  })
}

function delete_post(confession_id) {
  $.ajax({
    url: "/delete/",
    type: "POST",
    data: { id: confession_id },

    success: function(json) {
      alert(json.result + "\nYou will be redirected to homepage after pressing OK")
      location.href="/"
    },

    error: function(xhr, errmsg, err) {
      alert(xhr.status + ": " + xhr.responseText);
    }
  })
}

function load_post(page, scroll_position) {
  $.ajax({
    url: "/manage/",
    type: "POST",
    data: { page_number: page},

    success: function(data) {
      console.log("insanity check")
      console.log(data)
      $("#scroll").replaceWith(data);
      $('#scroll').scrollTop(scroll_position)
      // data = JSON.parse(json.query)
      // $('.confession-box').append('<div class="confession-heading"><p>' + data[0].confess_date + '</p></div><!-- Confession --><div class="confession-main"><p id="' + data[0].confess_date + '">' + data[0].confession_text + '</p></div><div class="confession-footer"><!-- Submit Button --><form method="post">{% csrf_token %}<button type="submit">Publish</button></form><!-- Edit Button --><form method="post" action="">{% csrf_token %}<button class="edit-button" type="submit" data-confession-id="' + data[0].pk + '" data-confession-text="' + data[0].confessions_text + '" data-session="{{  user }}">Edit</button></form></div>')
    },
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText);
    }
  });
}

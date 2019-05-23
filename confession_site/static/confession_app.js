function validateForm_content() {
    let content = document.forms["confess_form"]["confess_content"].value;
    if (content==="" || content==="Your Confession goes here") {
        alert("Please input something to submit the confession");
        return false;
    }
}

function edit_confession_text() {
  let content = JSON.parse(document.getElementById('confession_id').textContent);
  alert(content);
  return true;
}

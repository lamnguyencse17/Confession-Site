function validateForm_content() {
    let content = document.forms["confess_form"]["confess_content"].value;
    if (content==="" || content==="Your Confession goes here") {
        alert("Please input something to submit the confession");
        return false;
    }
}
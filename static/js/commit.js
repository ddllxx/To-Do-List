function click_commit(obj) {
    console.log(obj);
    title = obj.innerText;
    console.log(title);
    if (title == "Delete") {
        obj.form.action = "/delete"; 
    } else if (title == "Modify") {
        obj.form.action = "/change";
    }
    obj.form.submit();
}
let blogLink = document.querySelector(".copy-blog-link");
blogLink.querySelector("button").addEventListener("click", function(){
    let input = blogLink.querySelector("input.blog-link");
    input.select();
    document.execCommand("copy");
    blogLink.classList.add("active");
    window.getSelection().removeAllRanges();
    setTimeout(function(){
        blogLink.classList.remove("active");
    }, 25000);
});
function search(term) {
    const ul = document.getElementById("entries");
    const lis = ul.querySelectorAll("li.entry");

    lis.forEach(item => {
	    const text = item.querySelector("p").textContent.toLowerCase();
	    if(text.includes(term.toLowerCase())) {
	        item.style.display = '';
	    } else {
	        item.style.display = 'none';
	    }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    document
	.getElementById("search-bar")
	.addEventListener('input', function() {
            search(this.value);
	});
});


$(document).ready(function () {
    $("#search").keyup(function () {
        let str1 = ""
        let temp = $(this).val()
        for (let i = temp.length - 1; (i >= 0 && temp[i] != ' '); i--) {
            str1 += temp[i]
        }
        str1 = str1.split("").reverse().join("")
        $.ajax({
            url: "suggestion/" + str1,
            success: function s(result) {
                $("div > p").remove()
                const data = result.split("]");
                if (data.length === 1) return;
                let i, j;
                for (i = 0; i < 8; i++) {
                    let str = ""
                    for (j = 0; j < data[i].length; j++) {
                        if (data[i].charAt(j) === '\'' || data[i].charAt(j) === '[' || data[i].charAt(j) === ',')
                            continue
                        str += data[i].charAt(j);
                    }
                    div = document.getElementById("myDropdown");
                    div.style.display = ""
                    p = document.createElement('p')
                    p.className = "custom"
                    p.addEventListener('click', function handelclick(e) {
                        updateInput(e.target.childNodes[0].data)
                        let str1 = ""
                        for (let i = e.target.childNodes[0].data.length - 1; e.target.childNodes[0].data[i] != ' '; i--) {
                            str1 += e.target.childNodes[0].data[i]
                        }
                        $.ajax({
                            url: "suggestion/" + str1.split("").reverse().join(""),
                            success: function (result) {
                                s(result)
                            }
                        })
                    })
                    p.append(str)
                    div.appendChild(p)
                }
            },
            error: function () {
                $("div > p").remove()
            }
        });
    });
});

function updateInput(ish) {
    let temp = document.getElementById("search").value
    let i = 0;
    for (i = temp.length - 1; (i >= 0 && temp[i] != ' '); i--) { }
    let final = ""
    for (let j = 0; j <= i; j++) {
        final += temp[j]
    }
    document.getElementById("search").value = final + ish
}
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}
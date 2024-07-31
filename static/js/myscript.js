console.log("hello")
let x=document.getElementById("bbn");

let plusButton=document.getElementsByClassName("plus-cart");
console.log(plusButton)
 
Array.from(plusButton).forEach(e =>{
    e.addEventListener("click",() =>{
        let id =e.getAttribute("pid");
        console.log(id)
        let eml=e.parentNode.children[2]
        fetch(`/pluscart?prod_id=${encodeURIComponent(id)}`, {
            method: "GET"
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json(); // Assuming the server responds with JSON
        })
        .then(data => {
            console.log("data =", data);
            eml.innerText= data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount

            // You can update the UI here based on the response
        })
        .catch(error => {
            console.error("Fetch error:", error);
        })

    })

})


// minus cart button
const minuscart = document.getElementsByClassName("minus-cart");
Array.from(minuscart).forEach(e =>{
    e.addEventListener("click",() =>{
        let id =e.getAttribute("pid");
        console.log(id)
        let eml=e.parentNode.children[2]
        fetch(`/minuscart?prod_id=${encodeURIComponent(id)}`, {
            method: "GET"
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json(); // Assuming the server responds with JSON
        })
        .then(data => {
            console.log("data =", data);
            eml.innerText= data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount

            // You can update the UI here based on the response
        })
        .catch(error => {
            console.error("Fetch error:", error);
        })

    })

})


// remove all parentNode because we neet to edelet everyting from that row
const removecart = document.getElementsByClassName("remove-cart")
Array.from(removecart).forEach(e =>{
    e.addEventListener("click",() =>{
        let id =e.getAttribute("pid");
        console.log(id)
        let eml=e
        fetch(`/removecart?prod_id=${encodeURIComponent(id)}`, {
            method: "GET"
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json(); // Assuming the server responds with JSON
        })
        .then(data => {
            console.log("data =", data);
            eml.innerText= data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()  // there are 4 dive thats why i m written 4 time parentNde

            // You can update the UI here based on the response
        })
        .catch(error => {
            console.error("Fetch error:", error);
        })

    })

})



// wishlist button 

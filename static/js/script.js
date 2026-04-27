const API = "http://127.0.0.1:5000";

async function book() {
    const data = {
        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        service: document.getElementById("service").value,
        depth: document.getElementById("depth").value,
        location: document.getElementById("location").value
    };

    const res = await fetch(`${API}/booking`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    alert("Booking Created!");

    // WhatsApp auto open
    const wa = await fetch(`${API}/send-whatsapp`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const waData = await wa.json();
    window.open(waData.url, "_blank");
}

async function pay() {
    const res = await fetch(`${API}/create-order`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({amount: 500})
    });

    const order = await res.json();

    var options = {
        "key": "rzp_test_xxxxx",
        "amount": order.amount,
        "currency": "INR",
        "name": "Sri Yamuna Borewells",
        "order_id": order.id,
        handler: function () {
            alert("Payment Success");
        }
    };

    var rzp = new Razorpay(options);
    rzp.open();
}
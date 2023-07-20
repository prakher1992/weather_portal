//https://www.geeksforgeeks.org/how-to-get-city-name-by-using-geolocation/
function getCoordintes() {
    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };

    function success(pos) {
        var crd = pos.coords;
        var lat = crd.latitude.toString();
        var lng = crd.longitude.toString();
        var coordinates = [lat, lng];
        console.log(`Latitude: ${lat}, Longitude: ${lng}`);
        getCity(coordinates);
        return;

    }

    function error(err) {
        console.warn(`ERROR(${err.code}): ${err.message}`);
    }

    navigator.geolocation.getCurrentPosition(success, error, options);
}

// Step 2: Get city name
function getCity(coordinates) {
    var xhr = new XMLHttpRequest();
    var lat = coordinates[0];
    var lng = coordinates[1];

    // Paste your LocationIQ token below.
    xhr.open('GET', "https://us1.locationiq.com/v1/reverse.php?key=xxx&lat=" +
    lat + "&lon=" + lng + "&format=json", true);
    xhr.send();
    xhr.onreadystatechange = processRequest;
    xhr.addEventListener("readystatechange", processRequest, false);

    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            var city = response.address.city;
            console.log(city);
            const api_url ="/current_loc/"+city;
            console.log(api_url);
            async function getapi(url) {

                // Storing response
                const response = await fetch(url);

                // Storing data in form of JSON
                var data = await response.json();
                console.log(data);
                if (response) {
                    console.log(data.data);
                }
            }
            // Calling that async function
            getapi(api_url);
            return;
        }
    }
}

getCoordintes();
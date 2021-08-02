/** processForm: get data from form and make AJAX call to our API. */

async function processForm(evt) {
    evt.preventDefault()
    
    let body = {
        name: evt.target[0].value,
        year: evt.target[1].value,
        email: evt.target[2].value,
        color: evt.target[3].value
    }

    await axios({
        method: 'post',
        url: '/api/get-lucky-num',
        data: body
    })
    .then(response => {
        handleResponse(response)
    })
    .catch(error => {
        console.log("error: ", error)
    })

}

/** handleResponse: deal with response from our lucky-num API. */

function handleResponse(resp) {
    const errorBoxes = document.getElementsByTagName('B')
    Array.from(errorBoxes).map(box => box.innerText = '')

    const resultDiv = document.getElementById('lucky-results')
    resultDiv.innerText = ''

    if (resp.data.error) {
        let errorKeys = Object.keys(resp.data.error)
        errorKeys.map(errorName => {
            let bBox = document.getElementById(`${errorName}-err`)
            bBox.innerText = resp.data.error[errorName]
        })
    } else {
        resultDiv.innerText = `
        Your lucky number is ${resp.data.num.num} ${resp.data.num.fact}
        Your birth year ${resp.data.year.year} ${resp.data.year.fact}`
    }
}


$("#lucky-form").on("submit", processForm);

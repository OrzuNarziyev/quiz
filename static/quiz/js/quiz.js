"use strict";
const url = window.location.href,
    quizBox = document.getElementById('quiz-box'),
    numberList = document.getElementById('list_number'),
    scoreBox = document.getElementById('score-box'),
    resultBox = document.getElementById('result-box'),
    timerBox = document.getElementById('timer-box'),
    quizForm = document.getElementById('quiz-form'),
    csrf = document.getElementsByName('csrfmiddlewaretoken');
// number_list = document.getElementById('list_number'),
//


// window.addEventListener('beforeunload', function (e) {
//     // Cancel the event
//     e.preventDefault();
//     // Chrome requires returnValue to be set
//     e.returnValue = '';
//     console.log("hello cancel")
//
//     // Prompt the user to confirm if they want to leave the page
//     var confirmationMessage = 'Are you sure you want to leave this page?';
//     (e || window.event).returnValue = confirmationMessage; // Gecko + IE
//     return confirmationMessage; // Webkit, Safari, Chrome etc.
// });

let timer;

// window.addEventListener('beforeunload', function(event) {
//     event.preventDefault();
//     event.returnValue = 'Are you sure you want to leave this page?';
//     if (confirm('Are you sure you want to leave this page?')) {
//       sendData()
//     } else {
//       console.log('cancel')
//     }
//   });

const activateTimer = (time) => {

    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    timer = setInterval(() => {
        seconds--
        if (seconds < 0) {
            seconds = 59
            minutes--
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes
        } else {
            displayMinutes = minutes
        }
        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }

        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(() => {
                clearInterval(timer)
                alert('Time ower')
                sendData()
            })

        }
        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}


let options = {
    method: 'GET',
    mode: 'same-origin',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
    }
}

fetch(url + 'data', options)
    .then(response => response.json())
    .then(result => {

        const data = result.data
        let sum = 0


        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {

                sum++
                if (sum === 1) {
                    numberList.innerHTML += `
                    <span class="number_item active" data-number="${sum}">
                       ${sum}
                    </span>
                `
                } else {
                    numberList.innerHTML += `
                <span class="number_item " data-number="${sum}" data-last="0">
                       ${sum}
                   </span>
                `
                }

                // numberList.innerHTML += `
                //    <span class="number_item selected" data-number="${sum}">
                //        ${sum}
                //    </span>
                // `

                var q = document.createElement('div')
                if (sum === 1) {
                    q.className = 'wrapper_question show mb-3'
                } else {
                    q.className = 'wrapper_question mb-3'
                }

                q.id = `question_${sum}`
                q.dataset.index = sum
                q.innerHTML = `<p>${sum}) ${question}</p>`
                answers.forEach(answer => {
                    q.innerHTML += `
                     <div class="abcd">
                                <input type="radio" class="answer" id="${answer.q_uid}-${answer.uuid}" name="${answer.q_uid}" value="${answer.uuid}">
                                <label for="${answer.q_uid}-${answer.uuid}">${answer.text}</label>
                     </div>
                    `
                })
                if (sum === data.length) {

                    q.innerHTML += `
                        <div class="d-flex justify-content-start mt-3 gap-3">
                        <button type="button" class="prev_btn arrow  px-8" data-arrow="${sum - 1}" data-current="${sum}">oldingi</button>
                        </div>
                        <br>
                        <div class="d-flex justify-content-center">
                        <button type="submit" class="prev_btn float-end  px-8">Testni yakunlash</button>
                            </div>
                        `
                } else if (sum === 1) {
                    q.innerHTML += `
                        <div class="d-flex justify-content-end mt-3 gap-3">
                        <button type="button" class="prev_btn arrow  px-8" data-arrow="${sum + 1}" data-current="${sum}"">keyingisi</button>
                        </div>
                        `
                } else {
                    q.innerHTML += `
                        <div class="d-flex justify-content-between mt-3 gap-3">
                        <button type="button" class="prev_btn arrow px-8" data-arrow="${sum - 1}" data-current="${sum}">oldingi</button>
                        <button type="button" class="prev_btn arrow  px-8" data-arrow="${sum + 1}" data-current="${sum}">keyingisi</button>
                        </div>
                        `

                }
                quizBox.appendChild(q)


            }
        })
        // quizBox.innerHTML+=`
        //                     <button type="submit" class="prev_btn  px-8">testni yakunlash</button>
        // `
        const
            numbers = numberList.querySelectorAll('[data-number]'),
            question_list = quizBox.querySelectorAll('[data-index]'),
            arrows = document.querySelectorAll('[data-arrow]');
        numbers.forEach((el, index) => {
            el.addEventListener('click', (event) => {
                event.preventDefault()

                // question_s = question_list[index]
                question_list.forEach((e, i) => {
                    if (i === index) {
                        question_list[index].classList.add('show')
                        el.classList.add('active')
                    } else {
                        if (numbers[i].classList.contains('active')) {
                            console.log("contain")
                            let items = [...question_list[i].getElementsByClassName('answer')]
                            items.forEach(item => {
                                if (item.checked) {
                                    numbers[i].classList.add('selected')
                                } else {
                                    console.log('dont cheaked')
                                }
                            })
                            if (numbers[i].checked) {
                                console.log('checked')
                                numbers[i].classList.add('selected')
                            }

                        }
                        question_list[i].classList.remove('show')
                        numbers[i].classList.remove('active')
                    }
                })
            })
        })
        arrows.forEach(el => {

            el.addEventListener('click', () => {
                console.log(el.dataset.current)
                numbers.forEach((item, index) => {
                    if (el.dataset.arrow - 1 == index) {

                        numbers[index].classList.add('active')
                        question_list[index].classList.add('show')

                        var q = [...question_list[el.dataset.current - 1].getElementsByClassName('answer')]
                        q.forEach(item => {
                            if (item.checked) {
                                numbers[el.dataset.current - 1].classList.add('selected')
                            } else {
                                console.log('dont cheaked')
                            }
                        })
                        // console.log(question_list[el.dataset.current])

                    } else {
                        numbers[index].classList.remove('active')
                        question_list[index].classList.remove('show')
                    }
                })
            })

        })
        activateTimer(result.time)
    })
    .catch((error) => {
        console.log(error)
    })


const sendData = () => {
    const elements = [...document.getElementsByClassName('answer')]
    clearTimeout(timer)
    const data = {}

    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })
    const send_options = {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf[0].value,
        },
        body: JSON.stringify({'data': data})
    }

    fetch(url + 'save', send_options)
        .then(response => response.json())
        .then(result => {
            var elem = document.getElementById('login');

            elem.innerHTML = `
             <div class="jumbotron">
                            <div class="">
                                <div class="">
                                    <h5 class="card-title">
                                        <h1></h1>
                                        <h3 class="display-6">${result.quiz}</h3>
                                    </h5>
                                    <hr class="my-4">
                                    <div class="responsive">
                                        <table class="table">

                                            <tr>
                                           
                                                <th>Umumiy savollar soni</th>
                                                <td>${result.count}</td>
                                            </tr>
                                            <tr>
                                                <th>Tog'ri javoblar</th>
                                                <td>${result.correct} / ${result.count}</td>
                                            </tr>
                                            <tr>
                                           
                                                <th>No to'g'ri belgilanganlar</th>
                                                <td>${result.wrong} </td>
                                            </tr>

                                            
                                            <tr>
                                                <th>Yig'ilgan ball</th>
                                                <td>${result.score}</td>
                                            </tr>
                                        </table>
                                    </div>
                                </div>

                            </div><!-- End Default Card -->


                            <a class="btn btn-primary btn-lg" href="/" role="button">Bosh sahifaga qaytish</a>
                        </div>
            `
        })


}

quizForm.addEventListener('submit', e => {
    e.preventDefault()
    sendData()
})

window.addEventListener('beforeunload', function (e) {
    // Cancel the event
    e.preventDefault();
    // Chrome requires returnValue to be set
    e.returnValue = '';
    // Show the alert message
});

// window.addEventListener('beforeunload', function (e) {
//     // Cancel the event
//     e.preventDefault();
//     // Chrome requires returnValue to be set
//     // confirm('Are you sure want to leave')
//     e.returnValue = '';
//     alert('horey')
//     console.log("hello cancel")
//
//     // Prompt the user to confirm if they want to leave the page
//     var confirmationMessage = 'Are you sure you want to leave this page?';
//     (e || window.event).returnValue = confirmationMessage; // Gecko + IE
//     return confirmationMessage; // Webkit, Safari, Chrome etc.
// });

window.addEventListener('unload', function () {
    // create an object with the data to be sent
    const data = {
        name: 'John Doe',
        email: 'johndoe@example.com'
    };
    sendData()
    // send the data using fetch API
    // fetch(url + 'fetch', {
    //     method: 'POST',
    //     body: JSON.stringify(data),
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': csrf[0].value,
    //
    //     }
    // })
    //     .then(response => {
    //         window.location.href = '/'
    //         console.log('Data sent successfully');
    //     })
    //     .catch(error => {
    //         console.error('Error sending data:', error);
    //     });
});

// window.addEventListener('unload', function (event) {
//     event.preventDefault();
//
//     event.returnValue = 'Are you sure you want to leave this page?';
//     fetch(url + 'fetch', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrf[0].value,
//         },
//         body: JSON.stringify({
//             data: 'some data'
//         })
//     });
//     if (confirm('Are you sure you want to leave this page?')) {
//
//     } else {
//         console.log('cancellllll')
//     }
// });

// window.addEventListener('beforeunload', function (event) {
//     event.preventDefault();
//     fetch(url + 'fetch', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             data: 'some data'
//         })
//     });
// });


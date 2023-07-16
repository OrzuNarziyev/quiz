let start__quiz_count = document.getElementById('start__count_quiz')
let end__quiz_count = document.getElementById('end__count_quiz')
let result_count = document.getElementById('count_result')
let employers_count = document.getElementById('employers_count')
let next_list_quiz_action = document.querySelectorAll('.next-item-quiz')
let prev_list_quiz_action = document.querySelectorAll('.prev-item-quiz')
let list_result_action = document.querySelectorAll('.item-result');
let org = document.getElementById('organization_results')


var options = {
    method: 'GET',
    mode: 'same-origin',
    headers: {
        "Content-Type": "application/json",
    }
}

fetch(url, options)
    .then(response => response.json())
    .then(data => {
        var next_test = data.test__next
        var prev_test = data.test__prev
        var cnt = data.data_res
        var name = data.data_name
        let max_count = Math.max(next_test.day, prev_test.month, data.result, data.users)
        arr_list = Object.values(cnt)
        console.log(data)
        arr_list.unshift(['score', 'organization'])

        var card = `<div class="col">
                <div class='card'>
                    <div class="card-body">
                        <h5 class="card-title">${name}</h5>
                        <div id='org-1' style="min-height: 400px;" class="echart"></div>
                    </div>
                </div>
            </div>`
        org.insertAdjacentHTML('afterbegin', card)
        echarts.init(document.querySelector(`#org-1`)).setOption({
            dataset: {
                source: arr_list
            },
            grid: {containLabel: true},
            xAxis: {name: '_'},
            yAxis: {type: 'category'},
            visualMap: {
                orient: 'horizontal',
                left: 'center',
                min: 0,
                max: 100,
                // text: ['High Score', 'Low Score'],
                // Map the score column to color
                dimension: 0,
                inRange: {
                    color: ['#F5F5F5', '#1B6B93', '#071952']
                }
            },
            series: [
                {
                    type: 'bar',
                    encode: {
                        // Map the "amount" column to X axis.
                        x: 'score',
                        // Map the "product" column to Y axis
                        y: 'organization'
                    }
                }
            ]
        });
        var i = 0

        function showCount() {

            i++
            console.log(data.result)

            if (i <= next_test.day) {
                start__quiz_count.innerHTML = i
            } else if (next_test.day === 0) {
                start__quiz_count.innerHTML = 0
            }
            if (i <= prev_test.month) {
                end__quiz_count.innerHTML = i
            } else if (prev_test.month === 0) {
                end__quiz_count.innerHTML = 0
            }

            if (i <= data.result) {
                result_count.innerHTML = i
            } else if (data.result === 0) {
                result_count.innerHTML = 0
            }


            if (i <= data.users) {
                employers_count.innerHTML = i
            } else if (data.users === 0) {
                employers_count.innerHTML = 0
            }
            let timer = setTimeout(showCount, 50);
            if (i >= max_count) {
                console.log('clear')
                clearInterval(timer)
            }

        }


        // showCount(result_count, data.result)
        // showCount(start__quiz_count, next_test.day)
        // showCount(end__quiz_count, prev_test.month)

        // start__quiz_count.innerHTML = next_test.day
        // end__quiz_count.innerHTML = prev_test.month
        //
        //
        // result_count.innerHTML = data.result
        // employers_count.innerHTML = data.users


        // showCount(result_count, data.result)
        // showCount(start__quiz_count, next_test.day)
        // showCount(end__quiz_count, prev_test.month)

        // showTime(employers_count, data.users)
        // showTime(employers_count, data.users)

        // tugallanmagan testlar ro'yxati
        next_list_quiz_action.forEach(el => {
            el.addEventListener('click', (event) => {
                if (el.dataset.action == 'next_today') {
                    console.log('start')
                    start__quiz_count.innerHTML = next_test.day
                }
                if (el.dataset.action == 'next_month') {
                    console.log('month')
                    start__quiz_count.innerHTML = next_test.month
                }
                if (el.dataset.action == 'next_year') {
                    console.log('year')
                    start__quiz_count.innerHTML = next_test.year
                }
            })
        });

        // tugallangan testlar ro'yxati'
        prev_list_quiz_action.forEach(el => {
            el.addEventListener('click', (event) => {
                if (el.dataset.action == 'prev-month') {
                    end__quiz_count.innerHTML = prev_test.month
                }
                if (el.dataset.action == 'prev-year') {
                    end__quiz_count.innerHTML = prev_test.year
                }
            })
        });

        showCount()


        // list_result_action.forEach(el => {
        //     el.addEventListener('click', (event) => {
        //         if (el.dataset.action == 'today') {
        //             result_count.innerHTML = data.result.day
        //         }
        //         if (el.dataset.action == 'month') {
        //             result_count.innerHTML = data.result.month
        //         }
        //         if (el.dataset.action == 'year') {
        //             result_count.innerHTML = data.result.year
        //         }
        //     })
        // })

    })
    .catch(error => {
        console.log('error')
    })
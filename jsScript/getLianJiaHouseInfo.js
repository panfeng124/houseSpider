// 获取所有的 <li> 节点
const listItems = document.querySelectorAll('.listContent > li');
const houseDatas = []
// 遍历每个 <li> 节点
listItems.forEach((listItem) => {
    // 获取楼盘名字
    const titleElement = listItem.querySelector('.title a');
    const estateName = titleElement ? titleElement.textContent.split(' ')[0] : null;

    // 获取面积
    const areaElement = listItem.querySelector('.title a');
    const areaText = areaElement ? areaElement.textContent.match(/(\d+\.\d+)平米/) : null;
    const area = areaText ? parseFloat(areaText[1]) : null;

    // 获取交易时间
    const dealDateElement = listItem.querySelector('.dealDate');
    const dealDate = dealDateElement ? dealDateElement.textContent : null;

    // 获取交易价格
    const totalPriceElement = listItem.querySelector('.totalPrice .number');
    const totalPrice = totalPriceElement ? parseFloat(totalPriceElement.textContent) : null;

    // 获取是否精装
    const houseInfoElement = listItem.querySelector('.houseInfo');
    const isRefurbished = houseInfoElement && houseInfoElement.textContent.includes('精装');

    // 获取挂牌价
    const dealCycleTxtElement = listItem.querySelector('.dealCycleTxt');
    const listingPriceText = dealCycleTxtElement ? dealCycleTxtElement.textContent.match(/挂牌(\d+)万/) : null;
    const listingPrice = listingPriceText ? parseFloat(listingPriceText[1]) : null;

    houseDatas.push({
        "楼盘名字": estateName,
        "面积": area,
        "交易时间": dealDate,
        "交易价格": totalPrice,
        "是否精装": isRefurbished,
        "挂牌价": listingPrice,
    })

});


function postData(houseDatas) {
    /*const data = {
        "address": "abc", "info": {
            "楼盘名字": "示例楼盘",
            "面积": "100平",
            "交易时间": "2025-04-14",
            "交易价格": "100万",
            "是否精装": "是",
            "挂牌价": "120万"
        }
    };*/
    console.log("postData:", postData)
    //houseName是python注入的
    const data = {
        "address": "蜀南春郡", "info": houseDatas
    };


    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/post_data', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log('数据发送成功：', xhr.responseText);
            } else {
                console.error('数据发送失败，状态码：', xhr.status);
            }
        }
    };

    xhr.send(JSON.stringify(data));
}

postData(houseDatas);

function nextUrl() {
    const data = {
        "url": "https://segmentfault.com/channel/frontend",
    };

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/nextUrl', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log('数据发送成功：', xhr.responseText);
            } else {
                console.error('数据发送失败，状态码：', xhr.status);
            }
        }
    };

    xhr.send(JSON.stringify(data));
}

//nextUrl()
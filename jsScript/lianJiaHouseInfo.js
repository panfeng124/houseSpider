// 获取当前 URL
const currentUrl = window.location.href;
// 判断当前 URL 是否以指定字符串开头
const isMatch = currentUrl.startsWith('https://clogin.lianjia.com/');


if (isMatch) {
    console.log('当前 是登录页面');
} else {
    console.log('当前 URL 不以 "https://clogin.lianjia.com/" 开头');

// 获取所有的 <li> 节点
    const listItems = document.querySelectorAll('.listContent > li');
    const houseDatas = []
// 遍历每个 <li> 节点
    listItems.forEach((listItem) => {

        // 获取楼盘名字
        const titleElement = listItem.querySelector('.title a');
        const estateName = titleElement ? titleElement.textContent.split(' ')[0] : null;
        if (arePlaceNamesSimilar(houseName, estateName)) {
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
                //"区域": houseArea,
            })
        }
    });

    function postData() {
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

        //houseName是python注入的
        const data = {
            "address": houseName, "info": houseDatas
        };

        if (isInit && houseDatas.length > 0) {
            let lastHouse = houseDatas[houseDatas.length - 1]
            if (isGreaterThanYear(lastHouse["交易时间"])) {
                const pagesButton = document.querySelectorAll('.page-box.house-lst-page-box > a');
                let pages = pagesButton.length > 4 ? 4 : pagesButton.length
                console.log(pageNum, pages, pagesButton.length)
                if (pageNum <= 4 && pages > pageNum) {
                    data.nextPage = pageNum + 1;
                }
            }
        }
        console.log("data:", data)


        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://127.0.0.1:5000/add_data', true);
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

    postData();
}

//判读啊时间大于2024
function isGreaterThanYear(dateString, year = 2024) {
    // 将输入的日期字符串转化为 Date 对象
    const date = new Date(dateString);

    // 创建一个指定年份的日期对象，这里用的是指定年份的1月1日
    const compareDate = new Date(year, 0, 1); // 比如 2024-01-01

    // 比较两个日期对象的时间戳
    return date > compareDate;
}

//楼盘名字相似度判断1
function getJaccardSimilarity(str1, str2) {
    // 将字符串转化为集合，去除重复的字符
    const set1 = new Set(str1.split(''));
    const set2 = new Set(str2.split(''));

    // 计算交集
    const intersection = new Set([...set1].filter(x => set2.has(x)));

    // 计算并集
    const union = new Set([...set1, ...set2]);

    // 返回Jaccard相似度
    return intersection.size / union.size;
}

//楼盘名字相似度判断2
function arePlaceNamesSimilar(name1, name2, threshold = 0.6) {
    // 使用Jaccard相似度计算地名相似度
    const similarity = getJaccardSimilarity(name1, name2);

    // 如果相似度高于阈值，则认为是相似的地名
    return similarity >= threshold;
}

//nextUrl()
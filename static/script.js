let chartsLoaded = { sentiment: false, wordcloud: false };
let chartInterval = setInterval(checkCharts, 2000);

function checkCharts() {
    fetch('/sentiment_chart')
        .then(response => {
            if (response.ok) {
                document.getElementById('sentimentChart').src = '/sentiment_chart';
                document.getElementById('sentimentChart').style.display = 'block';
                document.getElementById('sentimentChartMessage').style.display = 'none';
                chartsLoaded.sentiment = true;
                stopIfChartsLoaded();
            }
        });

    fetch('/wordcloud_chart')
        .then(response => {
            if (response.ok) {
                document.getElementById('wordcloudChart').src = '/wordcloud_chart';
                document.getElementById('wordcloudChart').style.display = 'block';
                document.getElementById('wordcloudChartMessage').style.display = 'none';
                chartsLoaded.wordcloud = true;
                stopIfChartsLoaded();
            }
        });
}

function stopIfChartsLoaded() {
    if (chartsLoaded.sentiment && chartsLoaded.wordcloud) {
        clearInterval(chartInterval);
    }
}

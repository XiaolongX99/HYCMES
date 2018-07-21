
$(document).ready(function(){
    
    BaseCompCharts();

});

var BaseCompCharts = function(){

    var initChartsFlot = function(){
        // Get the elements where we will attach the charts
        var $flotLive       = jQuery('.js-flot-live');
        // Live Chart
        var $dataLive = [];

        function getRandomData() { // Random data generator

            if ($dataLive.length > 0)
                $dataLive = $dataLive.slice(1);

            while ($dataLive.length < 300) {
                var prev = $dataLive.length > 0 ? $dataLive[$dataLive.length - 1] : 50;
                var y = prev + Math.random() * 10 - 5;
                if (y < 0)
                    y = 0;
                if (y > 100)
                    y = 100;
                $dataLive.push(y);
            }

            var res = [];
            for (var i = 0; i < $dataLive.length; ++i)
                res.push([i, $dataLive[i]]);

            // Show live chart info
            jQuery('.js-flot-live-info').html(y.toFixed(0) + '%');

            return res;
        }

        function updateChartLive() { // Update live chart
            $chartLive.setData([getRandomData()]);
            $chartLive.draw();
            setTimeout(updateChartLive, 70);
        }

        var $chartLive = jQuery.plot($flotLive, // Init live chart
            [{ data: getRandomData() }],
            {
                series: {
                    shadowSize: 0
                },
                lines: {
                    show: true,
                    lineWidth: 2,
                    fill: true,
                    fillColor: {
                        colors: [{opacity: .2}, {opacity: .2}]
                    }
                },
                colors: ['#75b0eb'],
                grid: {
                    borderWidth: 0,
                    color: '#aaaaaa'
                },
                yaxis: {
                    show: true,
                    min: 0,
                    max: 110
                },
                xaxis: {
                    show: false
                }
            }
        );

        updateChartLive(); // Start getting new data

        
    return {
        init: function () {

            initChartsFlot();

        }
    };
}();
};

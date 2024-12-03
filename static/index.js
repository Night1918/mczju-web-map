AMapLoader
    .load({
        key: "3e0f56e6660823c03ec8ca25efa21781",
        version: "2.0",
    })
    .then((AMap) => {
        const layer = new AMap.createDefaultLayer({
            zooms: [3, 20],
            visible: true,
            opacity: 1,
            zIndex: 0,
        });
        const map = new AMap.Map("container", {
            viewMode: "3D",
            zoom: 15,
            center: [120.08184, 30.302721],
            features: ["bg", "building"],
            isHotspot: false,
            layers: [layer],
        });
        const imageLayer = new AMap.ImageLayer({
            url: "/static/map.png",
            bounds: new AMap.Bounds([120.0622, 30.29285], [120.0954, 30.3145]),
            zIndex: 2,
            zooms: [12, 20],
        });
        map.add(imageLayer);
        AMap.plugin(["AMap.ToolBar", "AMap.Scale", "AMap.ControlBar"], function () {
            map.addControl(new AMap.ToolBar());
            map.addControl(new AMap.Scale());
            map.addControl(
                new AMap.ControlBar({
                    position: "RT",
                })
            );
        });
        fetch("/api/data")
            .then((response) => response.json())
            .then((data) => {
                data.forEach((item) => {
                    const polygon = new AMap.Polygon({
                        path: JSON.parse(item.path),
                        fillColor: item.color,
                        strokeOpacity: 1,
                        fillOpacity: 0.6,
                        strokeColor: item.color,
                        strokeWeight: 1,
                        strokeStyle: "dashed",
                        strokeDasharray: [5, 5],
                    });
                    const infoWindowContent = `
                        <div class='area-info'>
                            <strong>${item.name}</strong><br>
                            ${item.info}<br>
                            ${item.status}<br>
                            ${item.detail}<br>
                            <button onclick="location.href='edit?id=${item.id}';" class="edit-button">编辑</button>
                        </div>
                    `;
                    const infoWindow = new AMap.InfoWindow({
                        isCustom: true,
                        content: infoWindowContent,
                        position: JSON.parse(item.position),
                        autoMove: true,
                        closeWhenClickMap: true,
                    });
                    polygon.on("click", () => {
                        infoWindow.open(map);
                    });
                    map.add(polygon);
                });
            })
            .catch((error) => {
                console.error("获取数据失败:", error);
            });
    })
    .catch((e) => {
      console.error(e);
    });
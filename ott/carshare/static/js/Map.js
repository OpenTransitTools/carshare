/**
 * 
 */
WGS_SRS = "EPSG:4326";
WEB_SRS = "EPSG:900913";

/** 
 * creates an OpenLayers.LonLat ojbect
 * transforms the coordinates if need be (e.g., 4326 -> 900913)
 *  
 * @param {Object} lon
 * @param {Object} lat
 * @param {Object} from_prj (optional)
 * @param {Object} to_prj (optional)
 */
function get_lon_lat(lon, lat, from_prj, to_prj)
{
    var ll = new OpenLayers.LonLat(lon, lat)
    if (from_prj && to_prj) 
        ll = ll.transform(from_prj, to_prj);
    
    return ll;
}


/**
 * center (and otionally zoom) the map to a lon/lat (X/Y) coordinate
 * 
 * @param {Object} map
 * @param {Object} lon
 * @param {Object} lat
 * @param {Object} zoom (optional)
 */
function center_map(map, lon, lat, zoom)
{
    var c = get_lon_lat(lon, lat, WGS_SRS, map.getProjectionObject())
    map.setCenter(c, zoom);
}

/**
 * create an OpenLayers basemap
 * 
 * @param {Object} wmsc_urls
 * @param {Object} num_zooms
 */
function make_ol_map(wmsc_urls, num_zooms)
{
    var osm_att = "Map data © <a href='http://www.openstreetmap.org/copyright' target='_blank'>OpenStreetMap</a> contributors. ";

    // resolutions for different zoom layers in OpenLayers (needed to restrict zoom to city)
    var ol_rez = [ 
        156543.03390000000945292413, 
        78271.51695000000472646207, 
        39135.75847500000236323103, 
        19567.87923750000118161552, 
        9783.93961875000059080776, 
        4891.96980937500029540388, 
        2445.98490468750014770194, 
        1222.99245234375007385097, 
        611.49622617187503692548, 
        305.74811308593751846274, 
        152.87405654296875923137, 
        76.43702827148437961569, 
        38.21851413574218980784, 
        19.10925706787109490392, 
        9.55462853393554745196, 
        4.77731426696777372598, 
        2.38865713348388686299, 
        1.19432856674194343150, 
        0.59716428337097171575,
        0.29858214168548585787,
        0.14929107084274292894,
        0.07464553542137146447,
        0.03732276771068573223,
        0.01866138385534286612,
        0.00933069192767143306
    ];

    // default tilecache is MapQuest ...
    if (!wmsc_urls)
    {
        osm_att = osm_att + " Tiles courtesy of <a href='http://open.mapquest.com/' target='_blank'>MapQuest</a>"
        wmsc_urls = [
                   "http://otile2.mqcdn.com/tiles/1.0.0/osm/${z}/${x}/${y}.png",
                   "http://otile3.mqcdn.com/tiles/1.0.0/osm/${z}/${x}/${y}.png",
                   "http://otile4.mqcdn.com/tiles/1.0.0/osm/${z}/${x}/${y}.png"
        ];
        num_zooms = 9;
    }
    if(!num_zooms)
        num_zooms = 9;

    var tm_base_opts = {
       serverResolutions : ol_rez,
       maxResolution     : 76.43702827148437961569,
       numZoomLevels     : num_zooms,
       buffer            : 0,
       tileOptions       : {crossOriginKeyword: null},
       transitionEffect  : 'resize',
       attribution       : osm_att
    };
    var map = new OpenLayers.Map('map', tm_base_opts);
    var basemap = new OpenLayers.Layer.OSM("OSM Map", wmsc_urls, tm_base_opts)
    map.addLayer(basemap);

    return map;
}

/**
 * create a geojson vector layer
 * 
 * @param {Object} map
 * @param {Object} url
 * @param {Object} name (optional)
 */
function make_geojson_layer(map, url, name)
{
    if (!name) name = "GeoJSON";

    var vector = new OpenLayers.Layer.Vector(name, {
        projection: "EPSG:4326",
        strategies: [new OpenLayers.Strategy.Fixed()],
        protocol: new OpenLayers.Protocol.HTTP({
            url:  url,
            format: new OpenLayers.Format.GeoJSON()
        })
    });
    map.addLayer(vector);
    return vector;
}


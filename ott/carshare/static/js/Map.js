/**
 * 
 */
WGS_SRS = "EPSG:4326";
WEB_SRS = "EPSG:900913";

function get_lon_lat(lon, lat, from_prj, to_prj)
{
    var ll = new OpenLayers.LonLat(lon, lat)
    if (from_prj && to_prj) 
        ll = ll.transform(from_prj, to_prj);
    
    return ll;
}

function center_map(map, lon, lat, zoom)
{
    var c = get_lon_lat(lon, lat, WGS_SRS, map.getProjectionObject())
    if(!zoom)
        zoom = 2;
    map.setCenter(c, zoom);
}


function make_ol_map(wmsc_urls)
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

    // default tilecache is ...
    if(!wmsc_urls)
        wmsc_urls = [
            "http://maps5.trimet.org/tilecache/tilecache.py/1.0.0/currentOSM/${z}/${x}/${y}"
        ];

    var tm_base_opts = {
       serverResolutions : ol_rez,
       maxResolution     : 76.43702827148437961569,
       numZoomLevels     : 10,
       buffer            : 0,
       tileOptions       : {crossOriginKeyword: null},
       transitionEffect  : 'resize',
       attribution       : osm_att
    };
    var map = new OpenLayers.Map('map', tm_base_opts);
    var basemap = new OpenLayers.Layer.OSM("TriMet OSM Map", wmsc_urls, tm_base_opts)
    map.addLayer(basemap);

    return map;
}



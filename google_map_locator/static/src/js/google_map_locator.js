openerp.google_map_locator = function (instance){

    //Widget for FormView
    instance.geo = {};
    instance.geo.leadMapFormWidget = instance.web.form.FormWidget.extend({
        template: 'leadmap',

        start: function(){
            var self = this;
            console.log("selffffffffffffff", self);
            var r = this._super();
            var rendererOptions = {draggable: false};
            try {
                this.directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
                this.directionsService = new google.maps.DirectionsService();
                this.map;
                this.model = this.view.dataset.model;
                this.country = new google.maps.LatLng(55, -180);

                var orderId = [];
                $('#map-canvas').parents().find('.oe_list_content input:checked').each(function(i){
                    if ($(this).closest('tr').attr('data-id')){
                        orderId.push(parseInt($(this).closest('tr').attr('data-id')));
                    }
                });
                //var orderId = $('#map-canvas').parents().find('.oe_list_content input:checked').closest('tr').attr('data-id');
                console.log("orderidddddddddddddd", orderId);
                self.mapInit(orderId);

            } catch(err) {
            }
            return r;
        },
        mapInit: function(id){
            var self = this;

            this.lines = new instance.web.Model('crm.lead');
            var defs = [];
            this.waypoints = [];
            if (this.model == 'crm.lead'){
                this.lines.call('search', [[['id','in',id]]])
                .then(function(results){
                    _.each(results, function(val, index){
                        defs.push(self.lines.call('read', [[val], ['city', 'country_id', 'company_id']], {})
                            .then(function(result){
                                console.log("main resultttttttttttt", result);
                                self.waypoints.push(result[0]);
                            }));
                    });
                    $.when.apply($, defs).then(function(){
                        self.get_ltlg(self.waypoints);
                    });
                });
            }
        },

        get_ltlg: function(res){
            console.log("ressssssssssssss", res);
            var self = this;
            var mapOptions = {zoom: 4, center: this.country, mapTypeId: google.maps.MapTypeId.ROADMAP};
            var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

            // bounds of the desired area
           /* var allowedBounds = new google.maps.LatLngBounds(
                new google.maps.LatLng(55, -180),
                new google.maps.LatLng(-55, 180)
            );
            var boundLimits = {
                maxLat : allowedBounds.getNorthEast().lat(),
                maxLng : allowedBounds.getNorthEast().lng(),
                minLat : allowedBounds.getSouthWest().lat(),
                minLng : allowedBounds.getSouthWest().lng()
            };

            var lastValidCenter = map.getCenter();
            var newLat, newLng;
            google.maps.event.addListener(map, 'center_changed', function() {
                center = map.getCenter();
                if (allowedBounds.contains(center)) {
                    // still within valid bounds, so save the last valid position
                    lastValidCenter = map.getCenter();
                    return;
                }
                newLat = lastValidCenter.lat();
                newLng = lastValidCenter.lng();

                if(center.lng() > boundLimits.minLng && center.lng() < boundLimits.maxLng){
                    newLng = center.lng();
                }

                if(center.lat() > boundLimits.minLat && center.lat() < boundLimits.maxLat){
                    newLat = center.lat();
                }
               // map.panTo(new google.maps.LatLng(newLat, newLng));
            });
            //google.maps.event.addDomListener(window, 'load', mapInit);*/

            map.setOptions({ minZoom: 2, maxZoom: 10 });
            var geocoder =  new google.maps.Geocoder();
            var infowindow = new google.maps.InfoWindow();
            var marker, i;
            for (var i=0;i<res.length;i++){
                if (res[i].city) {
                    geocoder.geocode({ 'address': res[i].city}, function(results, status) {
                        console.log("\n resultsssssssssssssss", results);
                        if (status == google.maps.GeocoderStatus.OK) {
                            var ltlg = results[0].geometry.location.lat() + " , " +results[0].geometry.location.lng();
                        }
                        if (ltlg){
                            var location = [ltlg];
                            for (i = 0; i < location.length; i++) {
                                var loc = location[0].split(",") ;
                                marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(loc[0],loc[1]),
                                    map: map
                                });
                                google.maps.event.addListener(marker, 'click', (function(marker, i) {
                                    return function() {
                                        infowindow.setContent(results[0].address_components[0].short_name + "," + results[0].address_components[2].long_name);
                                        infowindow.open(map, marker);
                                    }
                                })(marker, i));
                            }
                        }
                    });
                } /*else {
                    $('#start').append("City is not define. Please add city into address.");
                }*/
            }
            // self.display()
        },
        /*display: function(){
            var self = this;
            self.directionsService.route(self.request, function(response, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                     self.directionsDisplay.setDirections(response);
                }
            });
        }*/

    });

    instance.web.form.custom_widgets.add('leadmap', 'instance.geo.leadMapFormWidget')

    instance.geo.MapFormWidget = instance.web.form.FormWidget.extend({
        template: 'map',

        start: function(){
            var self = this;
            var r = this._super();
            var rendererOptions = {draggable: false};
            try {
                this.directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
                this.directionsService = new google.maps.DirectionsService();
                this.map;
                this.model = this.view.dataset.model;
                this.country = new google.maps.LatLng(55, -180);
                var orderId = this.view.dataset.ids[0];
                self.mapInit(orderId);

            } catch(err) {
            }
            return r;
        },
        mapInit: function(id){
            var self = this;
            console.log("selffffffffffffff", self.$el.find());
            self.$el.find('.oe_form_group').remove();
            var mapOptions = {zoom: 10, center: this.country, mapTypeId: google.maps.MapTypeId.ROADMAP};
            this.map = new google.maps.Map(document.getElementById('tour-map-canvas'), mapOptions);
            this.directionsDisplay.setMap(this.map);
            var infowindow = new google.maps.InfoWindow({maxWidth: 300});
            var marker, i;

            this.lines = new instance.web.Model('crm.lead');
            var defs = [];
            this.waypoints = [];
            if (this.model == 'crm.lead'){
                this.lines.call('search', [[['id','in',[id]]]])
                .then(function(results){
                    _.each(results, function(val, index){
                        defs.push(self.lines.call('read', [[val], ['name','phone','city', 'country_id', 'company_id']], {})
                            .then(function(result){
                                self.waypoints.push(result[0]);
                            }));
                    });
                    $.when.apply($, defs).then(function(){
                        self.get_ltlg(self.waypoints);
                    });
                });
            }

            $('#distance').on('click', function(){
                console.log("way pointssss", self.waypoints[0]);
                if (self.waypoints[0].city){
                    self.calcRoute(self.waypoints);
                    google.maps.event.addListener(self.directionsDisplay, 'directions_changed', function() {
                        self.showSteps(self.directionsDisplay.getDirections());
                    });
                } else {
                    alert("Address Not Found.");
                }
            });

            
        },
        get_ltlg: function(res){
            var self = this;
            var mapOptions = {zoom: 4, mapTypeId: google.maps.MapTypeId.ROADMAP};
            var map = new google.maps.Map(document.getElementById('tour-map-canvas'), mapOptions);

            //map.setOptions({ minZoom: 2, maxZoom: 10, center: this.country});
            var geocoder =  new google.maps.Geocoder();
            var infowindow = new google.maps.InfoWindow({maxWidth: 300});
            var i;
            
            for (var i=0;i<res.length;i++){
                if (res[i].city) {
                    geocoder.geocode({ 'address': res[i].city}, function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                            var ltlg = results[0].geometry.location.lat() + " , " +results[0].geometry.location.lng();
                            console.log("\n ltlgltlgltlgltlgltlg", typeof(ltlg));
                        }
                        if (ltlg){
                            this.centermap = new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng());
                            map.setOptions({ minZoom: 2, center: this.centermap});
                            var location = [ltlg];
                            for (i = 0; i < location.length; i++) {
                                var loc = location[0].split(",") ;
                                self.marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(loc[0],loc[1]),
                                    map: map
                                });
                                google.maps.event.addListener(self.marker, 'click', (function(marker, i) {
                                    return function() {
                                        console.log("resultsssssssss", results[0]);
                                        infowindow.setContent(res[i].name + "<br/>" + (res[i].phone || '') + "<br/>" + results[0].address_components[0].short_name + "," + results[0].address_components[2].long_name);
                                        infowindow.open(map, marker);
                                    }
                                })(self.marker, i));
                            }
                        }
                    });
                } 
            }
        },
        calcRoute: function(results){
            var self = this;
            var location = [];
            self.request = {
                origin:'',
                destination:'',
                waypoints:[],
                travelMode: google.maps.TravelMode.DRIVING
            };
            this.model = new instance.web.Model('res.company');
            _.each(results, function(val, index){
                 if (!val.city && !val.company_id){
                    return ;
                }
                self.model.call('read', [[val.company_id[0]], ['city', 'street','zip','country_id']], {}).then(function(value){
                        var origin = val.city;
                        var destination = value[0].city;

                        if(value[0].city != false){
                            var street = value[0].city.replace(',','')
                            destination += ', ' + value[0].city;
                        }
                        if(value[0].zip != false){
                            destination += ', ' + value[0].zip;
                        }
                        if(value[0].country_id != false){
                            destination += ', ' + value[0].country_id[1];
                        }
                        self.request.origin = origin;
                        self.request.destination = destination;

                        self.request.waypoints.push({location: origin, stopover: true});
                        self.request.waypoints.push({location: destination, stopover: true});
                        if(index == results.length-1){
                            self.display();
                        };
                    });
            });

        },
        showSteps: function(response){
            var self = this;
            var output = '';
            var route = response.routes[0];

            var distance = self.computeTotalDistance(route);
            if (parseFloat(distance)){
                this.field_manager.fields['km'].set_value(parseFloat(distance.replace(',','.')));
            }
            else{
                this.field_manager.fields['km'].set_value(parseFloat(distance));
            }
            this.field_manager.fields['km']._dirty_flag = true;
            var dist_miles = parseFloat(distance) * 0.621371;
            self.$el.find('.oe_form_group').remove();
            $('#dist').html('<div><b>Distance:-</b> '+distance+ ' km <span style="color:red">('+dist_miles+' miles)</span></div>');
            $('#distance').attr('disabled','disabled');
            self.mapInit();
        },
        computeTotalDistance: function(route){
            var self = this;
            var total = 0;
            for (var i = 0; i < route.legs.length; i++){
                total += route.legs[i].distance.value;
            }
            total = total/1000;
            return total.toFixed(1).toString().replace('.',',');
        },
        display: function(){
            var self = this;
            self.directionsService.route(self.request, function(response, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                     self.directionsDisplay.setDirections(response);
                }
            });
        }

    });

    instance.web.form.custom_widgets.add('map', 'instance.geo.MapFormWidget')

};

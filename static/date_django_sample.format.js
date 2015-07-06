/**
 *
 * https://github.com/jacwright/date.format 에 기반하여 django l10n 에 맞춰 수정
 *
 **/

(function() {

    Date.shortMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    Date.abbrMonths = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'];
    Date.longMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    Date.shortDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    Date.longDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // defining patterns
    var replaceChars = {
        a: function() { return this.getHours() < 12 ? 'a.m.' : 'p.m.'; },
        A: function() { return this.getHours() < 12 ? 'AM' : 'PM'; },
        b: function() { return Date.shortMonths[this.getMonth()].toLowerCase(); },
        B: function() { return Math.floor((((this.getUTCHours() + 1) % 24) + this.getUTCMinutes() / 60 + this.getUTCSeconds() / 3600) * 1000 / 24); }, // Fixed now
        c: function() { return this.format("Y-m-d\\TH:i:sP"); }, // Fixed now
        d: function() { return (this.getDate() < 10 ? '0' : '') + this.getDate(); },
        D: function() { return Date.shortDays[this.getDay()]; },
        e: function() { return /\((.*)\)/.exec(new Date().toString())[1]; },
        // E: NotImplemented
        f: function() {
            var value = (this.getHours() % 12 || 12);
            if ( this.getMinutes() > 0 )
                value += ':' + replaceChars['i'].call(this);
            return value;
        },
        F: function() { return Date.longMonths[this.getMonth()]; },
        g: function() { return this.getHours() % 12 || 12; },
        G: function() { return this.getHours(); },
        h: function() { return ((this.getHours() % 12 || 12) < 10 ? '0' : '') + (this.getHours() % 12 || 12); },
        H: function() { return (this.getHours() < 10 ? '0' : '') + this.getHours(); },
        i: function() { return (this.getMinutes() < 10 ? '0' : '') + this.getMinutes(); },
        I: function() {
            var DST = null;
            for (var i = 0; i < 12; ++i) {
                var d = new Date(this.getFullYear(), i, 1);
                var offset = d.getTimezoneOffset();
                if (DST === null)
                    DST = offset;
                else if (offset < DST) {
                    DST = offset;
                    break;
                }
                else if (offset > DST)
                    break;
            }
            return (this.getTimezoneOffset() == DST) | 0;
        },
        j: function() { return this.getDate(); },
        l: function() { return Date.longDays[this.getDay()]; },
        L: function() {
            var year = this.getFullYear();
            return (year % 400 == 0 || (year % 100 != 0 && year % 4 == 0));
        },
        m: function() { return (this.getMonth() < 9 ? '0' : '') + (this.getMonth() + 1); },
        M: function() { return Date.shortMonths[this.getMonth()]; },
        n: function() { return this.getMonth() + 1; },
        N: function() { return Date.abbrMonths[this.getMonth()]; },
        o: function() {
            var d  = new Date(this.valueOf());
            d.setDate(d.getDate() - ((this.getDay() + 6) % 7) + 3);
            return d.getFullYear();
        },
        O: function() {
            return (-this.getTimezoneOffset() < 0 ? '-' : '+') +
                (Math.abs(this.getTimezoneOffset() / 60) < 10 ? '0' : '') +
                (Math.abs(this.getTimezoneOffset() / 60)) + '00';
        },
        P: function() {
            if ( this.getHours() == 0 )
                return 'midnight';
            else if ( this.getHours() == 12 )
                return 'noon';
            return replaceChars['f'].call(this) + ' ' + replaceChars['a'].call(this);
        },
        r: function() { return this.toString(); },
        s: function() { return (this.getSeconds() < 10 ? '0' : '') + this.getSeconds(); },
        S: function() {
            return (this.getDate() % 10 == 1 && this.getDate() != 11 ?
                    'st' : (this.getDate() % 10 == 2 && this.getDate() != 12 ?
                    'nd' : (this.getDate() % 10 == 3 && this.getDate() != 13 ? 'rd' : 'th')));
        },
        t: function() {
            var year = this.getFullYear(), nextMonth = this.getMonth() + 1;
            if (nextMonth === 12) {
                year = year++;
                nextMonth = 0;
            }
            return new Date(year, nextMonth, 0).getDate();
        },
        T: function() { return this.toTimeString().replace(/^.+ \(?([^\)]+)\)?$/, '$1'); },
        u: function() { var m = this.getMilliseconds(); return (m < 10 ? '00' : (m < 100 ? '0' : '')) + m; },
        U: function() { return this.getTime() / 1000; },
        w: function() { return this.getDay(); },
        W: function() {
            var target = new Date(this.valueOf());
            var dayNr = (this.getDay() + 6) % 7;
            target.setDate(target.getDate() - dayNr + 3);
            var firstThursday = target.valueOf();
            target.setMonth(0, 1);
            if (target.getDay() !== 4) {
                target.setMonth(0, 1 + ((4 - target.getDay()) + 7) % 7);
            }
            return 1 + Math.ceil((firstThursday - target) / 604800000);
        },
        y: function() { return ('' + this.getFullYear()).substr(2); },
        Y: function() { return this.getFullYear(); },
        z: function() { var d = new Date(this.getFullYear(),0,1); return Math.ceil((this - d) / 86400000); }, // Fixed now
        Z: function() { return -this.getTimezoneOffset() * 60; }
    };

    // Simulates PHP's date function
    Date.prototype.format = function(format) {
        var date = this;
        return format.replace(/(\\?)(.)/g, function(_, esc, chr) {
            return (esc === '' && replaceChars[chr]) ? replaceChars[chr].call(date) : chr;
        });
    };

}).call(this);

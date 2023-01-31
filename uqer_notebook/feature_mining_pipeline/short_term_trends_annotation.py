# -*- coding: utf-8 -*-
# 标注数据 周线中期趋势
stock_rdate = {
    "000016":
        [
            ("2007-07-06", "2007-09-04", +1),
            ("2007-09-04", "2007-11-12", -1),
            ("2007-11-12", "2008-01-04", +1),
            ("2008-01-04", "2008-04-03", +0),
            ("2008-04-03", "2008-05-05", +1),
            ("2008-05-05", "2008-10-28", -1),
            ("2008-10-28", "2009-04-16", +1),
            ("2009-04-16", "2009-09-29", +0),
            ("2009-09-29", "2009-12-04", +1),
            ("2009-12-04", "2010-03-25", +0),
            ("2010-03-25", "2010-07-02", -1),
            ("2010-07-02", "2010-08-26", +1),
            ("2010-08-26", "2010-11-09", +0),
            ("2010-11-09", "2011-01-25", -1),
            ("2011-01-25", "2011-04-14", +1),
            ("2011-04-14", "2011-08-09", -1),
            ("2011-08-09", "2011-11-23", +0),
            ("2011-11-23", "2012-01-06", -1),
            ("2012-01-06", "2013-09-26", +0),
            ("2013-09-26", "2014-02-20", +1),
            ("2014-02-20", "2014-04-21", +0),
            ("2014-04-21", "2014-06-04", -1),
            ("2014-06-04", "2015-06-11", +1),
            ("2015-06-11", "2015-09-28", -1),
            ("2015-09-28", "2015-12-07", +0),
            ("2015-12-07", "2016-01-29", -1),
            ("2016-01-29", "2017-05-11", +0),
            ("2017-05-11", "2017-11-10", +1),
            ("2017-11-10", "2018-04-04", +0),
            ("2018-04-04", "2018-10-19", -1),
            ("2018-10-19", "2019-01-30", +0),
            ("2019-01-30", "2019-03-21", +1),
            ("2019-03-21", "2019-06-06", -1),
            ("2019-06-06", "2019-12-02", +0),
            ("2019-12-02", "2020-03-11", +1),
            ("2020-03-11", "2020-05-28", -1),
            ("2020-05-28", "2022-01-06", +0),
            ("2022-01-06", "2022-04-27", -1),
            ("2022-04-27", "2022-07-01", +1),
            ("2022-07-01", "2022-12-16", +0),
        ],

    "600966":
        [
            ("2007-07-01", "2008-02-21", +1),
            ("2008-02-21", "2008-05-15", +0),
            ("2008-05-15", "2008-11-04", -1),
            ("2008-11-04", "2009-08-03", +1),
            ("2009-08-03", "2010-04-13", +0),
            ("2010-04-13", "2010-07-02", -1),
            ("2010-07-02", "2010-09-15", +1),
            ("2010-09-15", "2010-11-11", +0),
            ("2010-11-11", "2011-01-25", -1),
            ("2011-01-25", "2011-04-22", +1),
            ("2011-04-22", "2012-01-06", -1),
            ("2012-01-06", "2012-03-20", +1),
            ("2012-03-20", "2012-11-29", -1),
            ("2012-11-29", "2014-01-14", +0),
            ("2014-01-14", "2014-08-18", +1),
            ("2014-08-18", "2015-01-19", +0),
            ("2015-01-19", "2015-06-18", +1),
            ("2015-06-18", "2015-09-15", -1),
            ("2015-09-15", "2015-12-31", +1),
            ("2015-12-31", "2016-12-13", +0),
            ("2016-12-13", "2017-02-14", +1),
            ("2017-02-14", "2017-06-02", +0),
            ("2017-06-02", "2017-10-10", +1),
            ("2017-10-10", "2018-03-08", +0),
            ("2018-03-08", "2019-01-31", -1),
            ("2019-01-31", "2019-04-25", +1),
            ("2019-04-25", "2019-09-26", +0),
            ("2019-09-26", "2020-11-23", +1),
            ("2020-11-23", "2021-05-07", +0),
            ("2021-05-07", "2022-04-27", -1),
            ("2022-04-27", "2022-10-31", +0),
            ("2022-10-31", "2022-12-16", +1),
        ],

    # "000555":
    # [
    # ("2007-07-01", "2008-03-06", +0),
    # ("2008-03-06", "2008-11-03", -1),
    # ("2008-11-03", "2009-07-10", +1),
    # ("2009-07-10", "2009-09-02", -1),
    # ("2009-09-02", "2009-11-23", +1),
    # ("2009-11-23", "2010-01-27", +0),
    # ("2010-01-27", "2010-03-22", +1),
    # ("2010-03-22", "2010-05-21", -1),
    # ("2010-05-21", "2011-11-17", +0),
    # ("2011-11-17", "2012-01-06", -1),
    # ("2012-01-06", "2012-03-14", +1),
    # ("2012-03-14", "2012-06-21", +0),
    # ("2012-06-21", "2012-08-02", -1),
    # ("2012-08-02", "2012-11-30", +0),
    # ("2012-11-30", "2013-02-27", +1),
    # ("2013-02-27", "2013-04-17", +0),
    # ("2013-04-17", "2013-10-15", +1),
    # ("2013-10-15", "2014-04-29", +0),
    # ("2014-04-29", "2015-05-22", +1),
    # ("2015-05-22", "2015-09-07", -1),
    # ("2015-09-07", "2015-12-21", +1),
    # ("2015-12-21", "2016-11-04", +0),
    # ("2016-11-04", "2018-02-07", -1),
    # ("2018-02-07", "2022-02-23", +0),
    # ("2022-02-23", "2022-04-26", -1),
    # ("2022-04-26", "2022-12-16", +0),
    # ],

    "600037":
        [
            ("2007-07-01", "2008-03-06", +0),
            ("2008-03-06", "2008-11-04", -1),
            ("2008-11-04", "2009-03-09", +0),
            ("2009-03-09", "2009-08-06", +1),
            ("2009-08-06", "2009-10-29", +0),
            ("2009-10-29", "2010-01-19", +1),
            ("2010-01-19", "2010-11-05", +0),
            ("2010-11-05", "2012-12-04", -1),
            ("2012-12-04", "2014-01-13", +0),
            ("2014-01-13", "2014-04-24", +1),
            ("2014-04-24", "2014-07-25", +0),
            ("2014-07-25", "2014-10-21", +1),
            ("2014-10-21", "2015-01-05", +0),
            ("2015-01-05", "2015-06-15", +1),
            ("2015-06-15", "2015-11-26", +0),
            ("2015-11-26", "2016-02-29", -1),
            ("2016-02-29", "2017-11-27", +0),
            ("2017-11-27", "2018-10-18", -1),
            ("2018-10-18", "2019-01-31", +0),
            ("2019-01-31", "2019-03-22", +1),
            ("2019-03-22", "2020-04-29", +0),
            ("2020-04-29", "2020-07-10", +1),
            ("2020-07-10", "2020-10-13", +0),
            ("2020-10-13", "2021-02-08", -1),
            ("2021-02-08", "2021-05-24", +1),
            ("2021-05-24", "2021-10-28", -1),
            ("2021-10-28", "2022-12-16", +0),
        ],

    "000088":
        [
            ("2007-07-01", "2008-03-06", +0),
            ("2008-03-06", "2008-10-28", -1),
            ("2008-10-28", "2009-02-17", +1),
            ("2009-02-17", "2009-05-25", +0),
            ("2009-05-25", "2009-08-05", +1),
            ("2009-08-05", "2010-03-19", +0),
            ("2010-03-19", "2010-07-02", -1),
            ("2010-07-02", "2010-11-09", +0),
            ("2010-11-09", "2011-01-17", -1),
            ("2011-01-17", "2011-05-11", +1),
            ("2011-05-11", "2011-12-05", -1),
            ("2011-12-05", "2012-04-24", +1),
            ("2012-04-24", "2012-12-04", +0),
            ("2012-12-04", "2013-02-04", +1),
            ("2013-02-04", "2013-05-08", +0),
            ("2013-05-08", "2013-07-29", -1),
            ("2013-07-29", "2013-11-26", +1),
            ("2013-11-26", "2014-04-15", +0),
            ("2014-04-15", "2014-06-20", -1),
            ("2014-06-20", "2014-12-12", +1),
            ("2014-12-12", "2015-07-02", +0),
            ("2015-07-02", "2015-09-16", -1),
            ("2015-09-16", "2017-01-16", +0),
            ("2017-01-16", "2017-04-12", +1),
            ("2017-04-12", "2017-10-20", +0),
            ("2017-10-20", "2017-12-25", -1),
            ("2017-12-25", "2018-05-24", +0),
            ("2018-05-24", "2018-10-15", -1),
            ("2018-10-15", "2019-01-31", +0),
            ("2019-01-31", "2019-04-22", +1),
            ("2019-04-22", "2019-08-06", -1),
            ("2019-08-06", "2020-06-12", +0),
            ("2020-06-12", "2020-08-05", +1),
            ("2020-08-05", "2022-03-04", +0),
            ("2022-03-04", "2022-04-28", -1),
            ("2022-04-28", "2022-12-16", +0),
        ],

    "000682":
        [
            ("2007-07-01", "2008-03-06", +0),
            ("2008-03-06", "2008-11-07", -1),
            ("2008-11-07", "2009-05-27", +1),
            ("2009-05-27", "2009-09-29", +0),
            ("2009-09-29", "2010-04-08", +1),
            ("2010-04-08", "2010-07-02", -1),
            ("2010-07-02", "2011-07-06", +0),
            ("2011-07-06", "2012-01-05", -1),
            ("2012-01-05", "2014-04-29", +0),
            ("2014-04-29", "2014-10-20", +1),
            ("2014-10-20", "2015-02-10", +0),
            ("2015-02-10", "2015-06-12", +1),
            ("2015-06-12", "2017-08-08", +0),
            ("2017-08-08", "2018-10-19", -1),
            ("2018-10-19", "2019-03-22", +1),
            ("2019-03-22", "2019-08-09", -1),
            ("2019-08-09", "2021-07-28", +0),
            ("2021-07-28", "2021-12-16", +1),
            ("2021-12-16", "2022-04-27", -1),
            ("2022-04-27", "2022-08-24", +1),
            ("2022-08-24", "2022-12-16", +0),
        ],

    "600420":
        [
            ("2007-07-01", "2008-05-14", +0),
            ("2008-05-14", "2008-11-03", -1),
            ("2008-11-03", "2010-01-18", +1),
            ("2010-01-18", "2010-12-01", +0),
            ("2010-12-01", "2012-01-06", -1),
            ("2012-01-06", "2012-07-09", +1),
            ("2012-07-09", "2012-12-13", +0),
            ("2012-12-13", "2013-03-06", +1),
            ("2013-03-06", "2014-06-09", +0),
            ("2014-06-09", "2014-10-29", +1),
            ("2014-10-29", "2015-02-12", +0),
            ("2015-02-12", "2015-06-04", +1),
            ("2015-06-04", "2017-08-11", +0),
            ("2017-08-11", "2018-10-18", -1),
            ("2018-10-18", "2022-12-16", +0),
        ],

    "600783":
        [
            ("2007-07-01", "2007-10-18", +1),
            ("2007-10-18", "2008-01-24", +0),
            ("2008-01-24", "2008-11-06", -1),
            ("2008-11-06", "2009-09-14", +1),
            ("2009-09-14", "2010-10-19", +0),
            ("2010-10-19", "2011-07-21", +1),
            ("2011-07-21", "2012-01-06", -1),
            ("2012-01-06", "2012-05-08", +0),
            ("2012-05-08", "2012-12-04", -1),
            ("2012-12-04", "2013-12-03", +1),
            ("2013-12-03", "2014-10-27", +0),
            ("2014-10-27", "2015-06-02", +1),
            ("2015-06-02", "2016-11-28", +0),
            ("2016-11-28", "2018-10-19", -1),
            ("2018-10-19", "2019-03-25", +0),
            ("2019-03-25", "2019-08-06", -1),
            ("2019-08-06", "2020-11-23", +0),
            ("2020-11-23", "2021-08-02", -1),
            ("2021-08-02", "2022-12-16", +0),
        ],

    "002051":
        [
            ("2007-07-01", "2008-01-16", +0),
            ("2008-01-16", "2008-11-04", -1),
            ("2008-11-04", "2010-12-06", +1),
            ("2010-12-06", "2012-03-30", +0),
            ("2012-03-30", "2012-09-10", +1),
            ("2012-09-10", "2013-06-21", +0),
            ("2013-06-21", "2013-11-13", -1),
            ("2013-11-13", "2014-06-26", +0),
            ("2014-06-26", "2015-06-12", +1),
            ("2015-06-12", "2015-07-08", -1),
            ("2015-07-08", "2017-01-16", +0),
            ("2017-01-16", "2017-04-20", +1),
            ("2017-04-20", "2017-11-01", +0),
            ("2017-11-01", "2018-10-25", -1),
            ("2018-10-25", "2019-01-29", +0),
            ("2019-01-29", "2019-04-08", +1),
            ("2019-04-08", "2021-02-04", -1),
            ("2021-02-04", "2021-11-03", +0),
            ("2021-11-03", "2022-03-09", +1),
            ("2022-03-09", "2022-12-16", +0),
        ],

    "000811":
        [
            ("2007-07-01", "2008-03-26", 0),
            ("2008-03-26", "2008-06-20", -1),
            ("2008-06-20", "2008-11-04", +0),
            ("2008-11-04", "2009-05-08", +1),
            ("2009-05-08", "2009-12-18", +0),
            ("2009-12-18", "2010-09-20", +1),
            ("2010-09-20", "2011-11-16", +0),
            ("2011-11-16", "2012-09-26", -1),
            ("2012-09-26", "2013-07-09", +0),
            ("2013-07-09", "2014-02-18", +1),
            ("2014-02-18", "2014-05-19", -1),
            ("2014-05-19", "2015-06-02", +1),
            ("2015-06-02", "2015-07-09", -1),
            ("2015-07-09", "2016-06-15", +0),
            ("2016-06-15", "2017-05-02", +1),
            ("2017-05-02", "2018-10-18", -1),
            ("2018-10-18", "2019-02-01", +0),
            ("2019-02-01", "2019-04-23", +1),
            ("2019-04-23", "2019-08-15", -1),
            ("2019-08-15", "2020-03-09", +0),
            ("2020-03-09", "2020-05-26", -1),
            ("2020-05-26", "2020-08-19", +1),
            ("2020-08-19", "2020-11-02", -1),
            ("2020-11-02", "2021-06-16", +0),
            ("2021-06-16", "2021-08-13", +1),
            ("2021-08-13", "2022-12-16", +0),
        ],

    "002004":
        [
            ("2007-07-01", "2008-03-05", +0),
            ("2008-03-05", "2008-11-04", -1),
            ("2008-11-04", "2009-04-02", +1),
            ("2009-04-02", "2009-08-20", +0),
            ("2009-08-20", "2010-04-26", +1),
            ("2010-04-26", "2011-08-11", +0),
            ("2011-08-11", "2012-01-17", -1),
            ("2012-01-17", "2012-07-13", +1),
            ("2012-07-13", "2014-12-30", +0),
            ("2014-12-30", "2015-04-16", +1),
            ("2015-04-16", "2015-12-17", +0),
            ("2015-12-17", "2016-01-26", -1),
            ("2016-01-26", "2016-11-16", +0),
            ("2016-11-16", "2017-05-23", -1),
            ("2017-05-23", "2017-10-18", +0),
            ("2017-10-18", "2018-10-18", -1),
            ("2018-10-18", "2021-02-02", +0),
            ("2021-02-02", "2021-06-01", +1),
            ("2021-06-01", "2021-08-06", -1),
            ("2021-08-06", "2021-09-14", +1),
            ("2021-09-14", "2021-10-29", -1),
            ("2021-10-29", "2022-01-13", +0),
            ("2022-01-13", "2022-04-27", -1),
            ("2022-04-27", "2022-07-22", +1),
            ("2022-07-22", "2022-12-16", +0),
        ],

    "000758":
        [
            ("2007-07-01", "2007-10-15", +1),
            ("2007-10-15", "2007-12-18", -1),
            ("2007-12-18", "2008-03-08", +0),
            ("2008-03-08", "2008-11-04", -1),
            ("2008-11-04", "2009-08-04", +1),
            ("2009-08-04", "2010-07-05", +0),
            ("2010-07-05", "2010-11-03", +1),
            ("2010-11-03", "2011-07-15", +0),
            ("2011-07-15", "2011-12-19", -1),
            ("2011-12-19", "2012-03-22", +1),
            ("2012-03-22", "2012-07-31", -1),
            ("2012-07-31", "2013-09-24", +0),
            ("2013-09-24", "2014-01-30", -1),
            ("2014-01-30", "2014-06-19", +0),
            ("2014-06-19", "2015-06-15", +1),
            ("2015-06-15", "2016-05-12", +0),
            ("2016-05-12", "2016-07-11", +1),
            ("2016-07-11", "2017-08-09", +0),
            ("2017-08-09", "2018-10-19", -1),
            ("2018-10-19", "2019-06-03", +1),
            ("2019-06-03", "2019-11-12", -1),
            ("2019-11-12", "2021-07-02", +0),
            ("2021-07-02", "2021-09-13", +1),
            ("2021-09-13", "2022-01-27", -1),
            ("2022-01-27", "2022-12-16", +0),
        ],

    "000913":
        [
            ("2007-07-01", "2008-03-06", +0),
            ("2008-03-06", "2008-11-04", -1),
            ("2008-11-04", "2009-05-20", +1),
            ("2009-05-20", "2009-09-20", +0),
            ("2009-09-20", "2010-04-23", +1),
            ("2010-04-23", "2010-06-30", -1),
            ("2010-06-30", "2011-07-07", +0),
            ("2011-07-07", "2012-01-06", -1),
            ("2012-01-06", "2012-06-15", +0),
            ("2012-06-15", "2012-09-27", -1),
            ("2012-09-27", "2012-12-04", +0),
            ("2012-12-04", "2013-03-26", +1),
            ("2013-03-26", "2013-07-19", +0),
            ("2013-07-19", "2013-10-29", -1),
            ("2013-10-29", "2014-02-18", +1),
            ("2014-02-18", "2014-07-28", +0),
            ("2014-07-28", "2014-10-10", +1),
            ("2014-10-10", "2015-02-09", +0),
            ("2015-02-09", "2015-06-15", +1),
            ("2015-06-15", "2015-07-09", -1),
            ("2015-07-09", "2015-09-16", +0),
            ("2015-09-16", "2015-11-20", +1),
            ("2015-11-20", "2016-02-01", -1),
            ("2016-02-01", "2016-04-18", +1),
            ("2016-04-18", "2016-08-23", +0),
            ("2016-08-23", "2016-11-10", +1),
            ("2016-11-10", "2017-08-23", +0),
            ("2017-08-23", "2017-11-21", +1),
            ("2017-11-21", "2018-02-06", -1),
            ("2018-02-06", "2018-05-21", +0),
            ("2018-05-21", "2018-08-20", -1),
            ("2018-08-20", "2020-06-16", +0),
            ("2020-06-16", "2020-11-05", +1),
            ("2020-11-05", "2021-04-13", +0),
            ("2021-04-13", "2021-07-28", -1),
            ("2021-07-28", "2021-11-22", +0),
            ("2021-11-22", "2022-04-29", -1),
            ("2022-04-29", "2022-08-29", +1),
            ("2022-08-29", "2022-12-16", -1),
        ],

    "002171":
        [
            ("2007-09-21", "2008-11-07", -1),
            ("2008-11-07", "2009-07-27", +1),
            ("2009-07-27", "2010-09-21", +0),
            ("2010-09-21", "2011-03-24", +1),
            ("2011-03-24", "2012-12-05", -1),
            ("2012-12-05", "2014-04-28", +0),
            ("2014-04-28", "2015-06-03", +1),
            ("2015-06-03", "2017-09-12", +0),
            ("2017-09-12", "2018-10-19", -1),
            ("2018-10-19", "2020-02-04", +0),
            ("2020-02-04", "2020-07-13", +1),
            ("2020-07-13", "2020-11-23", +0),
            ("2020-11-23", "2021-02-05", -1),
            ("2021-02-05", "2021-05-24", +0),
            ("2021-05-24", "2021-08-31", +1),
            ("2021-08-31", "2021-12-31", +0),
            ("2021-12-31", "2022-04-27", -1),
            ("2022-04-27", "2022-08-19", +1),
            ("2022-08-19", "2022-10-27", +0),
            ("2022-10-27", "2022-12-16", -1),
        ],

    "002063":
        [
            ("2007-07-01", "2008-03-13", +0),
            ("2008-03-13", "2008-10-20", -1),
            ("2008-10-20", "2009-04-15", +1),
            ("2009-04-15", "2009-09-29", +0),
            ("2009-09-29", "2010-01-15", +1),
            ("2010-01-15", "2010-07-02", +0),
            ("2010-07-02", "2010-11-30", +1),
            ("2010-11-30", "2011-02-26", -1),
            ("2011-02-26", "2011-11-03", +0),
            ("2011-11-03", "2012-01-16", -1),
            ("2012-01-16", "2012-05-02", +0),
            ("2012-05-02", "2012-08-22", +1),
            ("2012-08-22", "2013-07-10", +0),
            ("2013-07-10", "2013-10-16", +1),
            ("2013-10-16", "2014-12-30", +0),
            ("2014-12-30", "2015-06-03", +1),
            ("2015-06-03", "2015-09-15", -1),
            ("2015-09-15", "2015-12-02", +1),
            ("2015-12-02", "2016-03-01", -1),
            ("2016-03-01", "2016-12-05", +0),
            ("2016-12-05", "2017-06-02", -1),
            ("2017-06-02", "2018-04-27", +0),
            ("2018-04-27", "2018-10-12", -1),
            ("2018-10-12", "2019-03-13", +1),
            ("2019-03-13", "2019-06-04", -1),
            ("2019-06-04", "2020-01-06", +1),
            ("2020-01-06", "2020-07-14", +0),
            ("2020-07-14", "2020-11-05", -1),
            ("2020-11-05", "2021-10-29", +0),
            ("2021-10-29", "2021-12-29", +1),
            ("2021-12-29", "2022-04-28", -1),
            ("2022-04-28", "2022-07-12", +1),
            ("2022-07-12", "2022-12-16", +0),
        ],

    "600477":
        [
            ("2007-07-01", "2007-10-08", -1),
            ("2007-10-08", "2008-03-06", +0),
            ("2008-03-06", "2008-08-27", -1),
            ("2008-08-27", "2009-09-30", +0),
            ("2009-09-30", "2009-11-19", +1),
            ("2009-11-19", "2011-11-08", +0),
            ("2011-11-08", "2012-12-04", -1),
            ("2012-12-04", "2014-03-17", +0),
            ("2014-03-17", "2014-04-22", +1),
            ("2014-04-22", "2015-02-06", +0),
            ("2015-02-06", "2015-06-16", +1),
            ("2015-06-16", "2016-03-07", +0),
            ("2016-03-07", "2016-06-27", -1),
            ("2016-06-27", "2016-10-13", +1),
            ("2016-10-13", "2017-01-16", +0),
            ("2017-01-16", "2017-05-08", +1),
            ("2017-05-08", "2017-07-26", +0),
            ("2017-07-26", "2017-09-05", +1),
            ("2017-09-05", "2018-02-09", -1),
            ("2018-02-09", "2018-04-03", +0),
            ("2018-04-03", "2018-07-20", -1),
            ("2018-07-20", "2019-04-09", +0),
            ("2019-04-09", "2019-11-12", -1),
            ("2019-11-12", "2020-08-10", +1),
            ("2020-08-10", "2022-04-27", +0),
            ("2022-04-27", "2022-08-01", +1),
            ("2022-08-01", "2022-11-01", -1),
            ("2022-11-01", "2022-12-16", +0),
        ],

}

stock_rdate_t = dict()
for key, val in stock_rdate.items():
    _len = len(val)
    stock_rdate_t[key] = (val[0][0], val[_len - 1][1])

print(stock_rdate_t)

label_annotation_dict = dict()

for key, val in stock_rdate.items():
    _ticker = key
    for idx, item in enumerate(val):
        _start_day, _end_day, _label = item
        if _ticker not in label_annotation_dict:
            label_annotation_dict[_ticker] = []
        _start_day = int(_start_day.replace("-", ""))
        _end_day = int(_end_day.replace("-", ""))
        _label = int(_label)
        stock_rdate[key][idx] = (_ticker, range(_start_day, _end_day + 1), _label)
        label_annotation_dict[_ticker].append((range(_start_day, _end_day + 1), _label))

print(label_annotation_dict.keys())
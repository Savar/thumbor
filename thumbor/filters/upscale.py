#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com


import thumbor.filters
from thumbor.filters import BaseFilter, filter_method
from thumbor.utils import logger


class Filter(BaseFilter):
    phase = thumbor.filters.PHASE_AFTER_LOAD

    @filter_method()
    def upscale(self):
        if not self.context.request.fit_in:
            logger.warning("filter:upscale was called without fit-in request")
            return

        orientation = self.context.request.engine.get_orientation()

        target_width = self.context.request.width
        target_height = self.context.request.height

        if self.context.config.RESPECT_ORIENTATION and orientation in [5, 6, 7, 8]:
            source_height, source_width = self.context.request.engine.size
        else:
            source_width, source_height = self.context.request.engine.size

        if source_width > target_width or source_height > target_height:
            logger.debug("filter:upscale was called but image is already big enough")
            return

        logger.warn("upscale was called (source_width/source_height = {0}/{1}) (target_width/target_height = {2}/{3})".format(source_width, source_height, target_width, target_height))

#2017-02-28 21:49:47 thumbor:WARNING upscale was called (source_width/source_height = 233/300) (target_width/target_height = 700/600)
#2017-02-28 21:49:47 thumbor:WARNING upscale result (width/height = 700/901.0)
#DEBUG source_width / target_width >= source_height / target_height

        if source_width * 1.0 / target_width >= source_height * 1.0 / target_height:
            self.context.request.height = int(round(source_height * target_width / source_width))
            self.context.request.width = target_width
        else:
            self.context.request.height = target_height
            self.context.request.width = int(round(source_width * target_height / source_height))

        self.context.request.fit_in = False
        logger.warn("upscale result (width/height = {0}/{1})".format(self.context.request.width, self.context.request.height))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/10 23:46
# @Author  : 0x00A0
# @File    : predict.py
# @Description : 封装的predictor类

import os
import sys
import asyncio
import asyncio, time, threading
from ppgan.apps import StyleGANv2EditingPredictor
from ppgan.apps import Pixel2Style2PixelPredictor


class predictor:
	def __init__(self, source_path, output_path, age):
		self.age = age
		self.path, self.filename = os.path.split(source_path)
		self.output_path = output_path
		self.p2s2p_predictor = Pixel2Style2PixelPredictor(
				output_path=self.output_path,
				weight_path=None,
				model_type='ffhq-inversion',
				seed=223,
				size=1024,
				style_dim=512,
				n_mlp=8,
				channel_multiplier=2)
		self.edit_predictor = StyleGANv2EditingPredictor(
				output_path=self.output_path,
				weight_path=None,
				model_type='ffhq-config-f',
				seed=None,
				size=1024,
				style_dim=512,
				n_mlp=2,
				channel_multiplier='age',
				direction_path=None)

	def predict(self):
		self.p2s2p_predictor.run(os.path.join(self.path, self.filename))
		self.edit_predictor.run(os.path.join(self.output_path, "dst.npy"), 'age', self.age)


if __name__ == '__main__':
	input_image = sys.argv[1]
	output_path = sys.argv[2]
	age = float(sys.argv[3])
	predictor = predictor(input_image, output_path, age)
	predictor.predict()

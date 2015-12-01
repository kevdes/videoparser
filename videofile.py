"""Object which contains specific header information from various video
formats"""
#
#  Copyright (c) 2007 Michael van Tellingen <michaelvantellingen@gmail.com>
#  All rights reserved.
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. The name of the author may not be used to endorse or promote products
#     derived from this software without specific prior written permission
# 
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


import datetime

from videoparser.version import version as __version__


__all__ = ['VideoFile', 'VideoStream', 'AudioStream']
__author__ = "Michael van Tellingen <michaelvantellingen at gmail.com>"
	
class VideoFile(object):

	def __init__(self):
		self._streams = {}
		self._format = ''
		
	def _add_stream(self, stream, index=None):
		if index is None:
			index = len(self._streams) + 1
		self._streams[index] = stream
	
	def get_stream(self, stream_index):
		return self._streams.get(stream_index)
	
	def set_container(self, format):
		self._format = format
		
	def new_video_stream(self, index=None):
		stream = VideoStream()
		self._add_stream(stream, index)
		return stream
	
	def new_audio_stream(self, index=None):
		stream = AudioStream()
		self._add_stream(stream, index)
		return stream
	
	def __repr__(self):
		buf =   " Container format: %s\n" % self._format 
		buf +=  " Streams: \n"
		
		for stream_index in self._streams:
			buf += "   %d (%s) => %s\n" % (stream_index,
									   self._streams[stream_index].type,
									   repr(self._streams[stream_index])
									   )
		
		return buf
	
	
	def get_video_streams(self):
		for stream_id in self._streams:
			if isinstance(self._streams[stream_id], VideoStream):
				yield self._streams[stream_id]
	video_streams = property(fget=get_video_streams)
	
	def get_audio_streams(self):
		for stream_id in self._streams:
			if isinstance(self._streams[stream_id], AudioStream):
				yield self._streams[stream_id]
	audio_streams = property(fget=get_audio_streams)


class VideoStream(object):
	""" Contains information from a video stream."""
	def __init__(self):
		self._duration = 0
		self._framerate = 0
		self._codec = ''
		self.type = 'Video'
		self._width = 0
		self._height = 0
		self._sourceTC = -1
		self._dropFrame = 0
		self._trackID = 0
		self._clean_aperture = None
		self._prod_aperture = None
		self._enc_aperture = None
		self._pasp = None
		self._clap = None
		self._gamma = None
		self._color_space = None
		self._field_type = 'Not set'
		self._field_order = 'Not set'

	def set_track_id(self, num):
		self._trackID = num
		
	def set_width(self, width):
		self._width = width
	
	def set_height(self, height):
		self._height = height
	
	def set_fields(self, field_type, field_order):
		if field_type == 1:
			self._field_type = 'Progressive'
			self._field_order = 'None'
		else:
			self._field_type = 'Interlaced'

		if field_order == 0:
				self._field_order = 'No Fields'
		elif field_order == 1: 
			'Top Field'
		elif field_order == 6:
			self._field_order = 'Bottom Field'
		elif field_order == 9:
			self._field_order = 'Top Field'
		elif field_order == 14: 
			self._field_order = 'Bottom Field'
		else:
			self._field_order = 'Unknown Field Order'

	def set_gama(self, gamma):
		self._gamma = gamma

	def set_pasp(self, pasp):
		if pasp == (1,1):
			self._pasp = '1:1'
		elif pasp == (10000, 7031) or pasp == (1024, 720):
			self._pasp = 'PAL 16x9'
		elif pasp == (59, 54):
			self._pasp = 'PAL 4x3'
		elif pasp == (10, 11):
			self._pasp = 'NTSC 4x3'
		elif pasp == (40, 33):
			self._pasp = 'NTSC 16x9'
		else:
			self._pasp = str(pasp[0]) + ':' + str(pasp[1]) + ' Unknown'

	def set_clap(self, clap):
		self._clap = clap

	def set_colr(self, colr):
		if colr == ('nclc', 1, 1, 1):
			self._color_space = 'HD'
		elif colr == ('nclc', 5, 1, 6):	
			self._color_space = 'PAL'
		elif colr == ('nclc', 6, 1, 6):	
			self._color_space = 'NTSC'
		else:
			self._color_space = 'Unknown'

	def set_codec(self, codec):
		self._codec = codec
	
	def set_framerate(self, framerate):
		self._framerate = framerate
		
	def set_duration(self, **kwargs):
		if 'seconds' not in kwargs and 'microseconds' not in kwargs:
			raise ValueError("Execpted seconds or microseconds keyword arg")
		self._duration = datetime.timedelta(**kwargs)
	
	def set_sourceTC(self, sourceTC):
		self._sourceTC = sourceTC
	
	def set_dropFrame(self, dropFrame):
		self._dropFrame = dropFrame
	
	def set_clean_aperture(self, aperture):
		self._clean_aperture = aperture

	def set_prod_aperture(self, aperture):
		self._prod_aperture = aperture

	def set_enc_aperture(self, aperture):
		self._enc_aperture = aperture

	def set_bitrate(self, bitrate):
		pass
	
	def set_codec_name(self, name):
		self._codec_name = name
	
	def set_codec_description(self, description):
		self._codec_description = description
		
	def __repr__(self):
		return "codec: %s, length: %s, resolution: %dx%d, fps: %s" % (
			self._codec, self._duration, self._width, self._height, self._framerate)


	def get_resolution(self):
		return (self._width, self._height)
	resolution = property(fget=get_resolution)
	
	def get_codec(self):
		return self._codec
	codec = property(fget=get_codec)
	
	def get_duration(self):
		return self._duration
	duration = property(fget=get_duration)
		
	
class AudioStream(object):
	""" Contains information from a audio stream."""
	def __init__(self):
		self._channels = 0
		self._codec = ''
		self._sample_rate = 0
		self._duration = 0
		self._bitrate = 0
		self._bits_per_sample = 0
		self.type = 'Audio'
		self._trackID = 0
		self._track_assignemnt = ''

	def set_track_id(self, num):
		self._trackID = num
	
	def set_track_assignment(self, assign):
		self._track_assignemnt = assign
	
	def set_channels(self, num):
		self._channels = num
	
	def set_codec(self, codec):
		self._codec = codec
	
	def set_sample_rate(self, rate):
		self._sample_rate = rate
	
	def set_bitrate(self, bitrate):
		self._bitrate = bitrate

	def set_bit_per_sample(self, bits):
		self._bits_per_sample = bits
		
	def set_duration(self, **kwargs):
		if 'seconds' not in kwargs and 'microseconds' not in kwargs:
			raise ValueError("Execpted seconds or microseconds keyword arg")
		#print kwargs
		self._duration = datetime.timedelta(**kwargs)

	def __repr__(self):
		return ("codec: %s, length: %s, channels: %d, sample-rate: %d, " +
			   "bit-rate: %s kb/s, Bits per sample: %s") % (
			self._codec, self._duration, self._channels, self._sample_rate,
			self._bitrate, self._bits_per_sample)

	
		


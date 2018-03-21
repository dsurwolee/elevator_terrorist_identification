from pylab import rcParams
from sklearn.model_selection import train_test_split
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers

class AutoencoderNN:
	"""
	""" 

	def __init__(self, dims=[], batch_size=15, nb_epoch=100):
		"""
		"""
		self.input_dim = dims[0]
		self.encoding_dim = dims[1]
		self.batch_size = batch_size
		self.nb_epoch = nb_epoch

	def model(self, inp_dim, enc_dim):
		"""
		"""
		input_layer = Input(shape=(inp_dim, ))
		encoder = Dense(enc_dim, activation='tanh', activity_regularizer=regularizers.l1(10e-5))(input_layer)
		encoder = Dense(int(enc_dim / 2), activation='relu')(encoder)
		decoder = Dense(int(enc_dim / 2), activation='tanh')(encoder)
		decoder = Dense(inp_dim, activation='relu')(decoder)
		autoencoder = Model(inputs=input_layer, outputs=decoder)
		return autoencoder

	def train(self, X_train):
		"""
		""" 
		autoencoder = self.model(self.input_dim, self.encoding_dim)
		autoencoder.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
		checkpointer = ModelCheckpoint(filepath='model.h5', verbose=0, save_best_only=True)
		tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0, write_graph=True, write_images=True)
		history = (autoencoder.fit(X_train, X_train, 
		                            epochs=self.nb_epoch,
		                            batch_size=self.batch_size, 
		                            shuffle=True,
		                            verbose=1,
		                            callbacks=[checkpointer, tensorboard]).history
		          )
		return autoencoder, history

	def predict(self, autoencoder, X):
		"""

		""" 
		return autoencoder.predict(X)

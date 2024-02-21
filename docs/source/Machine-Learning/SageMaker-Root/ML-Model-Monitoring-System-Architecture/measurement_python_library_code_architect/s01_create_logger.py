# -*- coding: utf-8 -*-

"""
This is a pseudo-code implementation of the model monitoring measurement library.
"""

import typing as T
import contextlib
from abc import ABC as AbstractClass, abstractmethod
import dataclasses


# ------------------------------------------------------------------------------
# Log Message data Model
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class StructMessage(AbstractClass):
    """
    Base data model for structured log message.
    """

    attribute_1: str = dataclasses.field()
    attribute_2: str = dataclasses.field()

    @abstractmethod
    def serialize(self) -> bytes:
        """
        Serialize structured message to binary data.
        """
        pass

    @abstractmethod
    @classmethod
    def deserialize(self, data: bytes) -> "StructMessage":
        """
        Deserialize binary data into structured message.
        """
        pass


Message = StructMessage


@dataclasses.dataclass
class JsonMessage(StructMessage):
    """
    Extend the base structured message class, base data model for json encoded log message.
    """


@dataclasses.dataclass
class BinaryMessage(StructMessage):
    """
    Extend the base structured message class, base data model for binary encoded log message.
    """


T_MESSAGE = T.Union[str, Message, JsonMessage, BinaryMessage]

# ------------------------------------------------------------------------------
# Logger Config
#
# Config object is a data container that holds the configuration of the logger.
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class LogHandlerConfig(AbstractClass):
    """
    Data model for log handler configuration.
    """


# ------------------------------------------------------------------------------
# Log Filter
#
# Log filter should
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class LogFilterConfig(AbstractClass):
    """
    Data model for log filter configuration.
    """

    @abstractmethod
    def filter(self, messages: T.Iterable[StructMessage]) -> T.Iterable[StructMessage]:
        """
        Filter log messages.
        """
        pass


@dataclasses.dataclass
class RegexFilter(LogFilterConfig):
    """
    filter by regex
    """

    invalid_patterns: T.List[str]
    valid_patterns: T.List[str]


@dataclasses.dataclass
class OperatorFilter(LogFilterConfig):
    """
    filter by custom operator function.
    """

    operator: T.Callable[[StructMessage], bool]


# ------------------------------------------------------------------------------
# Log Sink
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class LogSinkConfig(AbstractClass):
    """
    Data model for log sink configuration.
    """

    @abstractmethod
    def heart_beat(self):
        """
        Test connection to the sink.
        """
        pass

    @abstractmethod
    def write(self, message: T_MESSAGE):
        """
        Write the log to buffer. The buffer should be a persistent storage like
        an append only file. Even the process is dead, we can recover the log buffer.
        """
        ...

    @abstractmethod
    def send(self):
        """
        Send the log in the buffer to the sink. It should have retry, error handling
        logics.
        """
        pass


@dataclasses.dataclass
class StreamSink(LogSinkConfig):
    """
    Abstract class for any stream data sink.
    """


@dataclasses.dataclass
class AwsCloudWatchLogsSink(LogSinkConfig):
    """
    Write log data to AWS CloudWatch Logs.
    """


@dataclasses.dataclass
class KafkaSink(LogSinkConfig):
    """
    Write log data to Kafka.
    """


@dataclasses.dataclass
class KinesisStreamSink(LogSinkConfig):
    """
    Write log data to Kinesis Stream.
    """


# Log config
@dataclasses.dataclass
class LoggerConfig(AbstractClass):
    """
    Config object for logger.
    """

    log_handlers: T.List[LogHandlerConfig] = dataclasses.field(default_factory=list)
    log_filters: T.List[LogFilterConfig] = dataclasses.field(default_factory=list)
    log_sinks: T.List[LogSinkConfig] = dataclasses.field(default_factory=list)


# ------------------------------------------------------------------------------
# Logger
# ------------------------------------------------------------------------------
class Logger(AbstractClass):
    """
    Generic Logger.
    """

    @classmethod
    def create(
        cls,
        name: str,
        config: LoggerConfig,
    ):
        """
        A factory method to create a logger.

        Loading logger from config file is just a wrapper of this method.
        """
        raise NotImplementedError

    def debug(self, message: T.Union[str, Message]):
        raise NotImplementedError

    def info(self, message: T.Union[str, Message]):
        raise NotImplementedError

    def warn(self, message: T.Union[str, Message]):
        raise NotImplementedError

    def error(self, message: T.Union[str, Message]):
        raise NotImplementedError

    def critical(self, message: T.Union[str, Message]):
        raise NotImplementedError

    def _log(self, level: int, message: T.Union[str, Message]):
        raise NotImplementedError

    def deco(self, *args, **kwargs):
        """
        A decorator that can be placed on function, method to automatically
        log the information we are interested.
        """
        raise NotImplementedError

    def capture_inference(self, *args, **kwargs):
        """
        A decorator that can automatically log the ML inference input output,
        latency, payload size, and everything about the transaction of ML inference.
        It is a special version of the :meth:`deco`.

        Example::

            @logger.capture_inference(
                sink=[
                    CloudWatchLogsSink
                    KinesisStreamSink,
                ]
            )
            def model_fn(input_data):
                ...
        """
        raise NotImplementedError

    def capture_training_data_statistics(self, *args, **kwargs):
        """
        A decorator that can automatically log the ML model training data statistics
        information.
        It is a special version of the :meth:`deco`.

        Example::

            @logger.capture_training_data_statistics(
                sink=[
                    CloudWatchLogsSink
                    KinesisStreamSink,
                ]
            )
            def train_fn(x_train, y_train):
                ...
        """
        raise NotImplementedError

    @contextlib.contextmanager
    def capture_error(self, *args, **kwargs):
        """
        A context manager that can automatically log the error information.

        Example::

            with logger.capture_error():
               # your ML app code goes here
        """
        raise NotImplementedError

    @contextlib.contextmanager
    def capture_latency(self, *args, **kwargs):
        """
        A context manager that can automatically log the computational time information.

        Example::

            with logger.capture_latency():
               # your ML app code goes here
        """
        raise NotImplementedError

    # you could have more ``capture_xyz`` decorator


class CustomLogger1(Logger):
    pass


class CustomLogger2(Logger):
    pass

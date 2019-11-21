# CNLogging
主要用于解决Python2.7当中logging模块打印包含中文的基本数据类型输出不正确的问题。  
例如：  
```bash
>>> import logging
>>> logging.warn(("使用", "帮助"))
WARNING:root:('\xe4\xbd\xbf\xe7\x94\xa8', '\xe5\xb8\xae\xe5\x8a\xa9')
>>> logging.warn({"使用": "帮助"})
WARNING:root:{'\xe4\xbd\xbf\xe7\x94\xa8': '\xe5\xb8\xae\xe5\x8a\xa9'}
```
因为项目需要，有大量的中文数据需要log审查，自己写了一个对基本数据类型序列化处理的函数来解决这一问题，目前具体性能情况没有实际测试，只是为了一个功能的实现。肯定还有很多问题存在的，只是一个简单的实现，日后有机会再改进，如果有人看到这个能给出意见那更好了。

- 使用方法
  - 同logging模块使用方法相似，`basicCNLogging`和`getCNLogger`方法和logging模块中的`basicConfig`和`getLogger`类似。
# FlexLogging

主要采用一个observer pattern模式来动态的控制输出情况，这个还是依赖于python自身的logging模块，忘了当初为什么需要这么一个功能了。
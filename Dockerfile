# 使用官方的 OpenJDK 镜像作为基础镜像
FROM openjdk:17-jdk-slim

# 设置维护者信息（可选）自定义
LABEL maintainer="tangwang9527@gmail.com"

# 设置工作目录
WORKDIR /app

# 将当前目录下的 masfd-rl-start-0.0.1-SNAPSHOT.jar 复制到容器中的 /app 目录下   
COPY masfd-rl-start-0.0.1-SNAPSHOT.jar /app/masfd-rl-start-0.0.1-SNAPSHOT.jar

# 暴露应用程序运行所需的端口（如果有的话，请根据实际情况修改）
EXPOSE 8080

# 定义启动命令
ENTRYPOINT ["java", "-jar", "/app/masfd-rl-start-0.0.1-SNAPSHOT.jar"]

# 给构建的镜像指定标签
# 这一步骤是在构建镜像时使用的，而非Dockerfile的一部分
# 构建命令：docker build -t masfd-rl-simulator .
FROM ubuntu@sha256:84e77dee7d1bc93fb029a45e3c6cb9d8aa4831ccfcc7103d36e876938d28895b

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates=20240203 \
    cmake=3.28.3-1build7 \
    g++=4:13.2.0-7ubuntu1 \
    make=4.3-4.1build2 \
    && rm -rf /var/lib/apt/lists/*

COPY CMakeLists.txt /app/CMakeLists.txt
COPY data /app/data
COPY include /app/include
COPY src /app/src

RUN cmake -S /app -B /app/build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build /app/build -j2

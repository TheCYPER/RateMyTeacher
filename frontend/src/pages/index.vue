<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="11" md="10" lg="8" class="text-center">
        <v-row align="center" justify="center" class="mb-6">
          <v-col cols="12" sm="8" md="6" lg="4" class="text-center">
            <v-img
              src="/logo.png"
              alt="Logo"
              contain
              height="200"
              class="mx-auto"
            />
          </v-col>
        </v-row>
        <v-row justify="center" class="mb-8">
          <v-col cols="12">
            <h1 class="text-h3 font-weight-bold">Rate My Teacher</h1>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12">
            <v-row>
              <v-col cols="12" md="6">
                <v-card class="mx-auto" height="900" elevation="4" rounded="lg">
                  <v-card-title class="text-h5">
                    热门教师
                  </v-card-title>
                  <v-card-text>
                    <!-- 内容区域 -->
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="mx-auto" height="900" elevation="4" rounded="lg">
                  <v-card-title class="text-h5">
                    最新评价
                  </v-card-title>
                  <v-card-text>
                    <!-- 内容区域 -->
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
// Component logic here if needed
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>

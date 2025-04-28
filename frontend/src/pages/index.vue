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
                    Famous teachers
                  </v-card-title>
                  <v-card-text class="scrollable-content">
                    <TopReviews />
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="mx-auto" height="900" elevation="4" rounded="lg">
                  <v-card-title class="text-h5">
                    Latest reviews
                  </v-card-title>
                  <v-card-text class="scrollable-content">
                    <LatestReviews />
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
import TopReviews from '@/components/TopReviews.vue';
import LatestReviews from '@/components/LatestReviews.vue';
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.scrollable-content {
  height: calc(900px - 64px); /* 卡片高度减去标题高度 */
  overflow-y: auto;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.scrollable-content::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}
</style>

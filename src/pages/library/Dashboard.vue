<template>
  <div>
    <Header title="Dashboard" pretitle="library"></Header>
    <div class="row">
      <div class="col-12 col-lg-6 col-xl">
        <!-- Value  -->
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col">
                <!-- Title -->
                <h6 class="text-uppercase text-muted mb-2">
                  Total games
                </h6>

                <!-- Heading -->
                <span class="h2 mb-0">
                  573
                </span>
              </div>
              <div class="col-auto">
                <!-- Icon -->
                <span class="h2 fe fe-dollar-sign text-muted mb-0"></span>
              </div>
            </div>
            <!-- / .row -->
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6 col-xl">
        <!-- Hours -->
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col">
                <!-- Title -->
                <h6 class="text-uppercase text-muted mb-2">
                  Different games
                </h6>

                <!-- Heading -->
                <span class="h2 mb-0">
                  483
                </span>
              </div>
              <div class="col-auto">
                <!-- Icon -->
                <span class="h2 fe fe-briefcase text-muted mb-0"></span>
              </div>
            </div>
            <!-- / .row -->
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6 col-xl">
        <!-- Exit -->
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col">
                <!-- Title -->
                <h6 class="text-uppercase text-muted mb-2">
                  Withdraws
                </h6>

                <!-- Heading -->
                <span class="h2 mb-0">
                  832
                </span>
              </div>
              <div class="col-auto">
                <!-- Chart -->
                <div class="chart chart-sparkline">
                  <div class="chartjs-size-monitor">
                    <div class="chartjs-size-monitor-expand">
                      <div class=""></div>
                    </div>
                    <div class="chartjs-size-monitor-shrink">
                      <div class=""></div>
                    </div>
                  </div>
                  <canvas
                    class="chart-canvas chartjs-render-monitor"
                    id="sparklineChart"
                    style="display: block; width: 75px; height: 35px;"
                    width="75"
                    height="35"
                  ></canvas>
                </div>
              </div>
            </div>
            <!-- / .row -->
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6 col-xl">
        <!-- Time -->
        <div class="card">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col">
                <!-- Title -->
                <h6 class="text-uppercase text-muted mb-2">
                  Avg. Time per withdraw
                </h6>

                <!-- Heading -->
                <span class="h2 mb-0">
                  2:37
                </span>
              </div>
              <div class="col-auto">
                <!-- Icon -->
                <span class="h2 fe fe-clock text-muted mb-0"></span>
              </div>
            </div>
            <!-- / .row -->
          </div>
        </div>
      </div>
    </div>
    <!-- / .row -->
  </div>
</template>

<script>
import Header from '@/components/Header'
export default {
  name: 'Dashboard',
  components: { Header },
}
</script>

<style scoped></style>

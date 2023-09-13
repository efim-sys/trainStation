<style>
  /*noinspection CssUnknownTarget*/
  /*@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Roboto:wght@100&display=swap');*/
</style>

<script lang='ts'>
  // The ordering of these imports is critical to your app working properly
  import '@skeletonlabs/skeleton/themes/theme-seafoam.css';
  // If you have source.organizeImports set to true in VSCode, then it will auto change this ordering
  import '@skeletonlabs/skeleton/styles/skeleton.css';
  // Most of your app wide CSS should be put in this file
  import './app.postcss';

  // import './theme.postcss';


  import {AppShell, AppBar, FileDropzone, FileButton, RadioItem, RadioGroup} from '@skeletonlabs/skeleton';

  import shuffle from "./icons/shuffle.svelte";
  import trash from "./icons/trash3-fill.svelte";
  import image from "./icons/file-earmark-image-fill.svelte"
  import add from "./icons/cloud-plus-fill.svelte"
  import {onMount} from "svelte";
  let value: Number


  // import "bootstrap-icons/font/bootstrap-icons.min.css"

  let count = "неизвестно";
  setInterval(async () => {
    count = await (await fetch("http://192.168.4.1/data?type=people")).text()
  }, 500)


  const voltage = 3668;
  const percentage = 53;
  const id = "Test";

  let scheme: HTMLImageElement
  let img: String = ""
  fetch("http://192.168.4.1/map").then(x => x.text().then(i => img = i))

  function onChangeHandler(e: Event): void {
    let files = (<HTMLInputElement>e.target).files;
    if (files.length != 1) return;
    scheme.onload = () => {
      URL.revokeObjectURL(scheme.src);
    }
    scheme.src = URL.createObjectURL(files[0]);
    for (let sensor of sensors){
      if (sensor.element == undefined) return
      updateCoords(sensor.element, sensor.x, sensor.y)
    }
  }

  interface Sensor {
    id: Number,
    x: Number,
    y: Number,
    element?: HTMLButtonElement
  }

  let sensors: Sensor[] = [{id: 1, x: 0.2, y: 0.5}, {id: 2, x: 0.2, y: 0.5}, {id: 3, x: 0.2, y: 0.5}];

  let selected: Sensor = <Sensor>{};


  let schemeDiv: HTMLDivElement;
  let rect: DOMRect;

  let hasMounted = false;

  onMount(() => {
    hasMounted = true;
    rect = schemeDiv.getBoundingClientRect();
  })

  function updateCoords(elem: HTMLElement, relX: Number, relY: Number) {
      elem.style.setProperty("left", relX * rect.width + schemeDiv.offsetLeft + "px")
      elem.style.setProperty("top", relY * rect.height + schemeDiv.offsetTop + "px")
  }
  function onClickImage(e: MouseEvent): void {
    console.log("clicked")
    e.stopPropagation();
    e.preventDefault();
    if (selected == {}) return;


    let relX = (e.pageX - schemeDiv.offsetLeft) / rect.width;
    let relY = (e.pageY - schemeDiv.offsetTop) / rect.height;
    selected.x = relX;
    selected.y = relY;
    if (selected.element == undefined) return;
    updateCoords(selected.element, relX, relY);
    return;
  }

  function onClickSensor(e: MouseEvent): void {
    let s = <HTMLButtonElement>e.target;
    let sensor = sensors.find(v => v.id == Number(s.getAttribute("id")));
    sensor.element = s;
    selected = sensor;
  }

  function clearPeople() {
    fetch("http://192.168.4.1/edit?people=0")
  }
</script>

<!-- App Shell -->
<AppShell>
  <svelte:fragment slot="header">
    <!-- App Bar -->
    <AppBar>
      <svelte:fragment slot="lead">
<!--        <img src={} class="h-[8vmin]">-->
<!--        &nbsp;-->
        <strong class="text-xl uppercase">Управление датчиками контроля кол-ва посетителей</strong>
      </svelte:fragment>
    </AppBar>
  </svelte:fragment>
<!--  <svelte:fragment slot="sidebarLeft">-->
<!--  </svelte:fragment>-->
  <!-- Page Route Content -->




  <br>
  <h2>Напряжение батареи: {voltage} Вольт (~ {percentage} %)</h2>

  <br>
  <h1 id="counter">В здании {count} чел.</h1>
  <br>
  <button type="button" class="btn variant-filled" on:click={clearPeople}>
    <span><svelte:component this={trash} /></span>
    <span>Обнулить значения посетителей</span>
  </button>
<!--  <button type="button" class="btn variant-filled">-->
<!--    <span><svelte:component this={shuffle} /></span>-->
<!--    <span>Сменить тип (Вход/Выход)</span>-->
<!--  </button>-->

  <div bind:this={schemeDiv}>
    {#if hasMounted}
      {#each sensors as sensor}
        <button id={sensor.id} type="button" class="btn-icon variant-filled" style="position: absolute; left: {sensor.x * rect.width + schemeDiv.offsetLeft + 'px'}; top: {sensor.y * rect.height + schemeDiv.offsetTop + 'px'}" on:click={onClickSensor}>{sensor.id}</button>
      {/each}
      <slot />
    {/if}

    <img alt="" bind:this={scheme} on:click={onClickImage} draggable="false" src="{img}">
  </div>

  <FileButton name="files" on:change={onChangeHandler}>
    <span><svelte:component this={image} /></span>
    <span>Загрузить схему</span>
  </FileButton>
  <slot />
</AppShell>
